from cmath import log
import socket
import ssl
import logging
from datetime import datetime
from typing import Any, Dict

from utils.helpers import (
    process_config_file,
    send_completion_notifications,
    send_error_notifications,
    send_expire_notifications,
)

logger = logging.getLogger(__name__)

def check_ssl_cert_for_expiry(domain: str, conf_options: Dict[str, Any]) -> int:
    """
    Function that will take an individual domain and check it's SSL cert.
    """
    try:
        logger.debug(f"Checking SSL cert for {domain}")

        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                ssl_info = ssock.getpeercert()
                logger.debug(f"SSL info for {domain}: {ssl_info}")
                if ssl_info:
                    expiry_date = datetime.strptime(
                        str(ssl_info["notAfter"]), "%b %d %H:%M:%S %Y %Z"
                    )
                    logger.debug(f"Expiry date for {domain}: {expiry_date}")
                else:
                    raise ValueError("No SSL information returned.")
                delta = expiry_date - datetime.utcnow()
                logger.debug(f"Days until expiry for {domain}: {delta.days}")
        return delta.days
    except ssl.SSLCertVerificationError as e:
        logger.error(f"SSL Cert Verification Error: {e}")
        logger.error(f"Verify Message: {e.verify_message}")

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

    if conf_options["APP"]["DEBUG"]:
        logging.basicConfig(level=logging.DEBUG)

    for domain in conf_options["APP"]["DOMAINS"]:
        days = check_ssl_cert_for_expiry(domain, conf_options)
        send_expire_notifications(domain, days, conf_options)

    send_completion_notifications(conf_options)


if __name__ == "__main__":
    main()
