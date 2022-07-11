import json
from typing import Any, Dict

import requests


def send_expire_teams_message(
    domain: str, status: str, days: int, config_options: Dict[str, Any]
) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/teams/domain-expiry.json", "r") as f:
        payload = json.load(f)

    if days == 0:
        payload["attachments"][0]["content"]["body"][0][
            "text"
        ] = "The following domain's SSL certificate expires today:"
    elif days == -1:
        payload["attachments"][0]["content"]["body"][0][
            "text"
        ] = "The following domain's SSL certificate has expired:"
    payload["attachments"][0]["content"]["body"][1]["columns"][0]["items"][0][
        "text"
    ] = f"**Domain:**\n\n{domain}"
    payload["attachments"][0]["content"]["body"][1]["columns"][1]["items"][0][
        "text"
    ] = f"**Status:**\n\n{status}"

    payload = json.dumps(payload, indent=4)

    requests.request("POST", config_options["APP"]["TEAMS_WEBHOOK"], headers=headers, data=payload)


def send_completion_teams_message(config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/teams/script-complete.json", "r") as f:
        payload = json.load(f)

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["TEAMS_WEBHOOK_COMPLETION"], headers=headers, data=payload
    )


def send_error_teams_message(error: str, config_options: Dict[str, Any]) -> None:
    headers = {"Content-Type": "application/json"}

    with open("templates/teams/script-error.json", "r") as f:
        payload = json.load(f)

    payload["attachments"][0]["content"]["body"][1]["columns"][0]["items"][0][
        "text"
    ] = f"*Error:*\n{error}"

    payload = json.dumps(payload, indent=4)

    requests.request(
        "POST", config_options["APP"]["TEAMS_WEBHOOK_ERROR"], headers=headers, data=payload
    )
