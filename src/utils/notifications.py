import json
import requests
from datetime import datetime, timezone

def send_expire_discord_message(domain, status, config_options) -> None:
    headers = {
        'Content-Type': 'application/json'
    }

    with open("templates/domain-expiry.json", 'r') as f:
        payload = json.load(f)
    
    payload['embeds'][0]['fields'][0]['value'] = domain
    payload['embeds'][0]['fields'][1]['value'] = status
    payload['embeds'][0]['timestamp'] = datetime.now(tz=timezone.utc).isoformat()

    payload = json.dumps(payload, indent=4)

    response = requests.request("POST", config_options['APP']['DISCORD_WEBHOOK'], headers=headers, data=payload)

def send_completion_discord_message(config_options) -> None:
    headers = {
        'Content-Type': 'application/json'
    }

    with open("templates/script-complete.json", 'r') as f:
        payload = json.load(f)

    payload['embeds'][0]['timestamp'] = datetime.now(tz=timezone.utc).isoformat()

    payload = json.dumps(payload, indent=4)

    response = requests.request("POST", config_options['APP']['DISCORD_WEBHOOK_COMPLETION'], headers=headers, data=payload)

def send_error_discord_message(error, config_options) -> None:
    headers = {
        'Content-Type': 'application/json'
    }

    with open("templates/script-error.json", 'r') as f:
        payload = json.load(f)

    payload['embeds'][0]['fields'][0]['value'] = error
    payload['embeds'][0]['timestamp'] = datetime.now(tz=timezone.utc).isoformat()

    payload = json.dumps(payload, indent=4)

    response = requests.request("POST", config_options['APP']['DISCORD_WEBHOOK_ERROR'], headers=headers, data=payload)