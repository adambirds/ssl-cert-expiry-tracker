import socket
import ssl
from datetime import datetime
from typing import Any, Dict

from utils.helpers import (
    process_config_file,
    send_completion_notifications,
    send_error_notifications,
    send_expire_notifications,
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
            send_error_notifications(
                f"The domain {domain} has a self-signed-cert which isn't supported.", conf_options
            )
            return -2
        elif "certificate has expired" in e.verify_message:
            return -1
        else:
            send_error_notifications(
                f"The domain {domain} has this error: {e.verify_message}", conf_options
            )
            return -2
    except socket.gaierror:
        send_error_notifications(
            f"The domain {domain} has no website for us to check against.", conf_options
        )
        return -2
    except ValueError as e:
        send_error_notifications(f"The domain {domain} has this error: {e}", conf_options)
        return -2


def main() -> None:
    """
    Main Loop.
    """

    conf_options = process_config_file()

    for domain in conf_options["APP"]["DOMAINS"]:
        days = check_ssl_cert_for_expiry(domain, conf_options)
        send_expire_notifications(domain, days, conf_options)

    send_completion_notifications(conf_options)


if __name__ == "__main__":
    main()
