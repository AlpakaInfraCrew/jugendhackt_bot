from prometheus_client.parser import text_string_to_metric_families
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json
import requests
load_dotenv()
uk_url = os.getenv('UK_URL')
url = f"https://{uk_url}/metrics"
username = os.getenv('UK_USER')
password = os.getenv('UK_PASSWD')
status_mapping = {
    0: "DOWN",
    1: "UP",
    2: "PENDING",
    3: "MAINTENANCE"
}
status_data = []
response = requests.get(url, auth=HTTPBasicAuth(username, password))
if response.status_code == 200:
    data = response.text
    metrics = text_string_to_metric_families(data)
    for metric in metrics:
        if metric.type == 'gauge' and metric.name == 'monitor_status':
            for sample in metric.samples:
                monitor_name = sample.labels['monitor_name']
                monitor_status_numeric = int(sample.value)
                monitor_status_text = status_mapping.get(monitor_status_numeric, "UNKNOWN")
                status_data.append({
                    "monitor_name": monitor_name,
                    "monitor_status_text": monitor_status_text
                })
print(json.dumps(status_data))
