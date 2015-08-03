## godaddy-dyndns

Python script that updates GoDaddy A Records

### Required modules:
* requests
* pygodaddy

### Usage:
* Copy 'godaddy-dyndns.conf.default' to 'godaddy-dyndns.conf'
* Edit 'godaddy-dyndns.conf' to suit your needs
* (Optional) Create a cronjob, e.g.
`@hourly cd /path/to/godaddy-dyndns && python3 godaddy-dyndns.py`
