# 23.07.2015 pascal vermeulen
import configparser
import requests
import logging
import sys
try:
    from pygodaddy import GoDaddyClient
except ImportError:
    print("You need to install the pygodaddy library to use this script.", file=sys.stderr)
    sys.exit(1)

def get_public_ip(protocol=4):
    try:
        r = requests.get('http://ipv%s.myexternalip.com/raw' % protocol)
        logging.info("Retrieved public IP: {}".format(r.text.strip()))
        return r.text.strip()
    except:
        logging.error("Unable to retrieve public IP")
        logging.info("Exiting")
        sys.exit(1)

if __name__=="__main__":
    config = configparser.ConfigParser()
    config.read('godaddy-dyndns.conf')
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        filename=config.get('log', 'file'),
        level=config.get('log', 'level').upper())
    logging.info('Script started')
    domain = config.get('godaddy', 'domain')

    client = GoDaddyClient()
    if not client.login(config.get('godaddy', 'username'), config.get('godaddy', 'password')):
        logging.error("GoDaddy login failed")
        logging.info("Exiting")
        sys.exit(1)

    for record in list(client.find_dns_records(domain)):
        if record.hostname in config.get('godaddy', 'dns_records').split():
            ip = get_public_ip()
            if record.value == ip:
                logging.info("{}.{} - no need to update IP".format(record.hostname, domain))
            else:
                client.update_dns_record('%s.%s' % (record.hostname, domain), ip)
                logging.info("{}.{} - public IP set to {}".format(record.hostname, domain, ip))
    logging.info("Exiting")
