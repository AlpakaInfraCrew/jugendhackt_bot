# Alpaka Infra Crew Telegram Bot

A simple Telegram bot for Alpaka Infra Crew


## HowTo

**Requirements:**
- python3
- pip3
- Telegram Bot / Telegram Bot Token
- Uptime Kuma Instance
- Uptime Kuma API Key

- `git clone https://github.com/AlpakaInfraCrew/jugendhackt_bot`
- `cp example.env .env`
- edit .env with your favourite editor (i.e. `vim .env`)
- `pip install -r requirements.txt`
- `python bot.by`
- ...
- Profit!

## Install as service:

- `adduser telegrambot`
- `cd /home/telegrambot`
- `su telegrambot`
- `git clone https://github.com/AlpakaInfraCrew/jugendhackt_bot`
- `cd jugendhackt_bot`
- `cp example.env .env`
- edit .env with your favourite editor (i.e. `vim .env`)
- `exit`
- `cd /home/telegrambot/jugendhackt_bot`
- `pip install -r requirements.txt`
- `cp ./telegrambot.service /etc/systemd/system/telegrambot.service`
- `systemctl daemon-reload`
- `systemctl enable telegrambot.service`
- `systemctl start telegrambot.service`
- ...
- `journalctl -efu telegrambot`