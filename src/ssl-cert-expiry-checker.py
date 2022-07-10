from operator import contains
from utils.helpers import process_config_file
import socket
import ssl
from datetime import datetime
from utils.notifications import send_completion_discord_message, send_error_discord_message, send_expire_discord_message, send_completion_zulip_message, send_error_zulip_message, send_expire_zulip_message

def check_ssl_cert_for_expiry(domain, conf_options) -> int:
    """
    Function that will take an individual domain and check it's SSL cert.
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, "443")) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                ssl_info = ssock.getpeercert()
                expiry_date = datetime.strptime(ssl_info['notAfter'], "%b %d %H:%M:%S %Y %Z")
                delta = expiry_date - datetime.utcnow()
                return delta.days
    except ssl.SSLCertVerificationError as e:
        if "self signed certificate" in e.verify_message:
            print(f"The domain {domain} has a self-signed-cert which isn't supported.")
            if "Discord" in conf_options['APP']['NOTIFICATIONS']:
                send_error_discord_message(f"The domain {domain} has a self-signed-cert which isn't supported.", conf_options)
            if "ZulipAPI" in conf_options['APP']['NOTIFICATIONS']:
                send_error_zulip_message(f"The domain {domain} has a self-signed-cert which isn't supported.", conf_options)
            return -2
        elif "certificate has expired" in e.verify_message:
            return -1
    except socket.gaierror:
        print(f"The domain {domain} has no website for us to check against.")
        if "Discord" in conf_options['APP']['NOTIFICATIONS']:
                send_error_discord_message(f"The domain {domain} has no website for us to check against.", conf_options)
        if "ZulipAPI" in conf_options['APP']['NOTIFICATIONS']:
                send_error_zulip_message(f"The domain {domain} has no website for us to check against.", conf_options)
        return -2
        

def main() -> None:
    """
    Main Loop.
    """

    conf_options = process_config_file()

    for domain in conf_options['APP']['DOMAINS']:
        days = check_ssl_cert_for_expiry(domain, conf_options)
        if days >= 1 and days <= conf_options['APP']['EXPIRE_DAYS_THRESHOLD']:
            print(f"The domain {domain} has {days} days left.")
            if "Discord" in conf_options['APP']['NOTIFICATIONS']:
                send_expire_discord_message(domain, f"Expires in {days} days.", conf_options)
            if "ZulipAPI" in conf_options['APP']['NOTIFICATIONS']:
                send_expire_zulip_message(domain, f"is set to expires in {days} days.", conf_options)
        elif days == 0:
            print(f"The domain {domain} expires today.")
            if "Discord" in conf_options['APP']['NOTIFICATIONS']:
                send_expire_discord_message(domain, f"Expires today.", conf_options)
            if "ZulipAPI" in conf_options['APP']['NOTIFICATIONS']:
                send_expire_zulip_message(domain, f"expires today.", conf_options)
        elif days == -1:
            print(f"The domain {domain} has expired.")
            if "Discord" in conf_options['APP']['NOTIFICATIONS']:
                send_expire_discord_message(domain, f"Expired", conf_options)
            if "ZulipAPI" in conf_options['APP']['NOTIFICATIONS']:
                send_expire_zulip_message(domain, f"is expired.", conf_options)
    
    if 'Discord' in conf_options['APP']['NOTIFICATIONS']:
        send_completion_discord_message(conf_options)
    if 'ZulipAPI' in conf_options['APP']['NOTIFICATIONS']:
        send_completion_zulip_message(conf_options)

if __name__ == "__main__":
    main()