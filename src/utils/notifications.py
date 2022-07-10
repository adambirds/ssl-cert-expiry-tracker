import json
from datetime import datetime, timezone
from typing import Any, Dict

import requests
import zulip


def send_expire_discord_message(domain: str, status: str, config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/domain-expiry.json", "r") as f:
        payload = json.load(f)

    payload["embeds"][0]["fields"][0]["value"] = domain
    payload["embeds"][0]["fields"][1]["value"] = status
    payload["embeds"][0]["timestamp"] = datetime.now(tz=timezone.utc).isoformat()

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["DISCORD_WEBHOOK"], headers=headers, data=payload
    )


def send_completion_discord_message(config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/script-complete.json", "r") as f:
        payload = json.load(f)

    payload["embeds"][0]["timestamp"] = datetime.now(tz=timezone.utc).isoformat()

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["DISCORD_WEBHOOK_COMPLETION"], headers=headers, data=payload
    )


def send_error_discord_message(error: str, config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/script-error.json", "r") as f:
        payload = json.load(f)

    payload["embeds"][0]["fields"][0]["value"] = error
    payload["embeds"][0]["timestamp"] = datetime.now(tz=timezone.utc).isoformat()

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["DISCORD_WEBHOOK_ERROR"], headers=headers, data=payload
    )


def send_completion_zulip_message(config_options: Dict[str, Any]) -> None:
    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file=config_options["APP"]["ZULIP_BOT_FILE"])

    # Send a stream message
    request = {
        "type": "stream",
        "to": config_options["APP"]["ZULIP_STREAM"],
        "topic": "SSL Certificate Expiry Check Complete",
        "content": "All domain's SSL Certificates have been successfully checked for expiry.",
    }
    client.send_message(request)


def send_expire_zulip_message(domain: str, status: str, config_options: Dict[str, Any]) -> None:
    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file=config_options["APP"]["ZULIP_BOT_FILE"])

    # Send a stream message
    request = {
        "type": "stream",
        "to": config_options["APP"]["ZULIP_STREAM"],
        "topic": domain,
        "content": f"The SSL Certificate for the domain {domain} {status}",
    }
    client.send_message(request)


def send_error_zulip_message(error: str, config_options: Dict[str, Any]) -> None:
    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file=config_options["APP"]["ZULIP_BOT_FILE"])

    # Send a stream message
    request = {
        "type": "stream",
        "to": config_options["APP"]["ZULIP_ERROR_STREAM"],
        "topic": "SSL Certificate Expiry Check Error",
        "content": error,
    }
    client.send_message(request)
