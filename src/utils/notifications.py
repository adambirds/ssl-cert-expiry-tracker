import json
import requests
import zulip
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

def send_completion_zulip_message(config_options):
    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file=config_options['APP']['ZULIP_BOT_FILE'])

    # Send a stream message
    request = {
        "type": "stream",
        "to": config_options['APP']['ZULIP_STREAM'],
        "topic": "SSL Certificate Expiry Check Complete",
        "content": "All domain's SSL Certificates have been successfully checked for expiry." 
    }
    result = client.send_message(request)

def send_expire_zulip_message(domain, status, config_options):
    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file=config_options['APP']['ZULIP_BOT_FILE'])

    # Send a stream message
    request = {
        "type": "stream",
        "to": config_options['APP']['ZULIP_STREAM'],
        "topic": domain,
        "content": f"The SSL Certificate for the domain {domain} {status}"
    }
    result = client.send_message(request)

def send_error_zulip_message(error, config_options):
    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file=config_options['APP']['ZULIP_BOT_FILE'])

    # Send a stream message
    request = {
        "type": "stream",
        "to": config_options['APP']['ZULIP_ERROR_STREAM'],
        "topic": "SSL Certificate Expiry Check Error",
        "content": error 
    }
    result = client.send_message(request)