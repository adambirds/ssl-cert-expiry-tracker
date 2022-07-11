from typing import Any, Dict

import yaml

from utils.notifications.discord import (
    send_completion_discord_message,
    send_error_discord_message,
    send_expire_discord_message,
)
from utils.notifications.slack import (
    send_completion_slack_message,
    send_error_slack_message,
    send_expire_slack_message,
)
from utils.notifications.teams import (
    send_completion_teams_message,
    send_error_teams_message,
    send_expire_teams_message,
)
from utils.notifications.zulip import (
    send_completion_zulip_message,
    send_error_zulip_message,
    send_expire_zulip_message,
)


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
    if "Teams" in conf_options["APP"]["NOTIFICATIONS"]:
        send_error_teams_message(
            error,
            conf_options,
        )
    if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
        send_error_zulip_message(
            error,
            conf_options,
        )


def send_expire_notifications(domain: str, days: int, conf_options: Dict[str, Any]) -> None:
    if days >= 1 and days <= conf_options["APP"]["EXPIRE_DAYS_THRESHOLD"]:
        if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_discord_message(domain, f"Expires in {days} days.", conf_options)
        if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_slack_message(domain, f"Expires in {days} days.", days, conf_options)
        if "Teams" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_teams_message(domain, f"Expires in {days} days.", days, conf_options)
        if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_zulip_message(domain, f"is set to expires in {days} days.", conf_options)
    elif days == 0:
        if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_discord_message(domain, "Expires today.", conf_options)
        if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_slack_message(domain, "Expires today.", days, conf_options)
        if "Teams" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_teams_message(domain, "Expires today.", days, conf_options)
        if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_zulip_message(domain, "expires today.", conf_options)
    elif days == -1:
        if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_discord_message(domain, "Expired", conf_options)
        if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_slack_message(domain, "Expired.", days, conf_options)
        if "Teams" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_teams_message(domain, "Expired.", days, conf_options)
        if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
            send_expire_zulip_message(domain, "is expired.", conf_options)


def send_completion_notifications(conf_options: Dict[str, Any]) -> None:
    if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
        send_completion_discord_message(conf_options)
    if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
        send_completion_slack_message(conf_options)
    if "Teams" in conf_options["APP"]["NOTIFICATIONS"]:
        send_completion_teams_message(conf_options)
    if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
        send_completion_zulip_message(conf_options)
