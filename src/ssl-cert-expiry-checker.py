import socket
import ssl
from datetime import datetime
from typing import Any, Dict

from utils.helpers import process_config_file
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
from utils.notifications.zulip import (
    send_completion_zulip_message,
    send_error_zulip_message,
    send_expire_zulip_message,
)


def check_ssl_cert_for_expiry(domain: str, conf_options: Dict[str, Any]) -> int:
    """
    Function that will take an individual domain and check it's SSL cert.
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                ssl_info = ssock.getpeercert()
                if ssl_info:
                    expiry_date = datetime.strptime(
                        str(ssl_info["notAfter"]), "%b %d %H:%M:%S %Y %Z"
                    )
                else:
                    raise ValueError("No SSL information returned.")
                delta = expiry_date - datetime.utcnow()
        return delta.days
    except ssl.SSLCertVerificationError as e:
        if "self signed certificate" in e.verify_message:
            if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
                send_error_discord_message(
                    f"The domain {domain} has a self-signed-cert which isn't supported.",
                    conf_options,
                )
            if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
                send_error_slack_message(
                    f"The domain {domain} has a self-signed-cert which isn't supported.",
                    conf_options,
                )
            if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
                send_error_zulip_message(
                    f"The domain {domain} has a self-signed-cert which isn't supported.",
                    conf_options,
                )
            return -2
        elif "certificate has expired" in e.verify_message:
            return -1
        else:
            if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
                send_error_discord_message(
                    f"The domain {domain} has this error: {e.verify_message}",
                    conf_options,
                )
            if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
                send_error_slack_message(
                    f"The domain {domain} has this error: {e.verify_message}",
                    conf_options,
                )
            if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
                send_error_zulip_message(
                    f"The domain {domain} has this error: {e.verify_message}",
                    conf_options,
                )
            return -2
    except socket.gaierror:
        if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
            send_error_discord_message(
                f"The domain {domain} has no website for us to check against.", conf_options
            )
        if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
            send_error_slack_message(
                f"The domain {domain} has no website for us to check against.", conf_options
            )
        if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
            send_error_zulip_message(
                f"The domain {domain} has no website for us to check against.", conf_options
            )
        return -2
    except ValueError as e:
        if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
            send_error_discord_message(f"The domain {domain} has this error: {e}", conf_options)
        if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
            send_error_slack_message(f"The domain {domain} has this error: {e}", conf_options)
        if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
            send_error_zulip_message(f"The domain {domain} has this error: {e}", conf_options)
        return -2


def main() -> None:
    """
    Main Loop.
    """

    conf_options = process_config_file()

    for domain in conf_options["APP"]["DOMAINS"]:
        days = check_ssl_cert_for_expiry(domain, conf_options)
        if days >= 1 and days <= conf_options["APP"]["EXPIRE_DAYS_THRESHOLD"]:
            if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_discord_message(domain, f"Expires in {days} days.", conf_options)
            if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_slack_message(domain, f"Expires in {days} days.", days, conf_options)
            if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_zulip_message(
                    domain, f"is set to expires in {days} days.", conf_options
                )
        elif days == 0:
            if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_discord_message(domain, "Expires today.", conf_options)
            if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_slack_message(domain, "Expires today.", days, conf_options)
            if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_zulip_message(domain, "expires today.", conf_options)
        elif days == -1:
            if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_discord_message(domain, "Expired", conf_options)
            if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_slack_message(domain, "Expired.", days, conf_options)
            if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
                send_expire_zulip_message(domain, "is expired.", conf_options)

    if "Discord" in conf_options["APP"]["NOTIFICATIONS"]:
        send_completion_discord_message(conf_options)
    if "Slack" in conf_options["APP"]["NOTIFICATIONS"]:
        send_completion_slack_message(conf_options)
    if "ZulipAPI" in conf_options["APP"]["NOTIFICATIONS"]:
        send_completion_zulip_message(conf_options)


if __name__ == "__main__":
    main()
