import zulip
from typing import Dict, Any

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