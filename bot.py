from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import subprocess
import json

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Hallo! Du kannst jetzt den Jugend hackt / Alpaka Infra Crew Bot nutzen. Falls du nach deiner Chat ID gefragt wirst, die ist: {chat_id}. Du kannst sie aber auch jederzeit mit dem Kommando /id anzeigen lassen.')

async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'{chat_id}')

async def sso(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://auth.alpaka.space')

async def sourcecode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Meinen Sourcecode findest du hier: https://github.com/AlpakaInfraCrew/jugendhackt_bot')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    import subprocess
    python_path = "/usr/bin/python3"
    process = subprocess.Popen([python_path, "monitoring.py"], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output_lines = output.decode("utf-8").strip().split("\n")
    json_data_str = "".join(output_lines)
    try:
        status_data = json.loads(json_data_str)
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"Beim Parsen der Statusdaten ist ein Fehler aufgetreten: {str(e)}")
        return

    keyboard = []
    for item in status_data:
        status_icon = "✅" if item["monitor_status_text"] == "UP" else \
                      "🔴" if item["monitor_status_text"] == "DOWN" else \
                      "⚠️" if item["monitor_status_text"] == "PENDING" else \
                      "Ⓜ️" if item["monitor_status_text"] == "MAINTENANCE" else ""
        keyboard.append([InlineKeyboardButton(f"{status_icon} {item['monitor_name']}", callback_data=item['monitor_name'])])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Status der Überwachungen:", reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text("Um die Daten zu updaten, gib einfach nochmal /status ein, oder geh auf https://status.alpaka.network für die Live ansicht.")

async def ende(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("OK! Solltest du wieder mit mir kommunizieren wollen verwende einfach /start")
    await context.bot.close()

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", chat_id))
    application.add_handler(CommandHandler("sso", sso))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("ende", ende))
    application.add_handler(CommandHandler("source", sourcecode))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()
