from typing import Any, Dict

import yaml

from utils.notifications.discord import send_error_discord_message
from utils.notifications.slack import send_error_slack_message
from utils.notifications.zulip import send_error_zulip_message


def process_config_file() -> Dict[str, Any]:

    with open("config.yaml", "r") as stream:
        config_options = yaml.safe_load(stream)

    return config_options


def send_error_notifications(error: str, conf_options: Dict[str, Any]) -> None:
    if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
        send_error_discord_message(
            error,
            conf_options,
        )
    if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
        send_error_slack_message(
            error,
            conf_options,
        )
    if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
        send_error_zulip_message(
            error,
            conf_options,
        )
