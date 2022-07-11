import json
from typing import Any, Dict

import requests


def send_expire_slack_message(
    domain: str, status: str, days: int, config_options: Dict[str, Any]
) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/slack/domain-expiry.json", "r") as f:
        payload = json.load(f)

    if days == 0:
        payload["blocks"][0]["text"][
            "text"
        ] = "The following domain's SSL certificate expires today:"
    elif days == -1:
        payload["blocks"][0]["text"]["text"] = "The following domain's SSL certificate has expired:"
    payload["blocks"][2]["fields"][0]["text"] = f"*Domain:*\n{domain}"
    payload["blocks"][2]["fields"][1]["text"] = f"*Status:*\n{status}"

    payload = json.dumps(payload, indent=4)

    requests.request("POST", config_options["APP"]["SLACK_WEBHOOK"], headers=headers, data=payload)


def send_completion_slack_message(config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/slack/script-complete.json", "r") as f:
        payload = json.load(f)

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["SLACK_WEBHOOK_COMPLETION"], headers=headers, data=payload
    )


def send_error_slack_message(error: str, config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/slack/script-error.json", "r") as f:
        payload = json.load(f)

    payload["blocks"][2]["fields"][0]["text"] = f"*Error:*\n{error}"

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["SLACK_WEBHOOK_ERROR"], headers=headers, data=payload
    )
