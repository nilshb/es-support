import logging
import os
import datetime
import requests
from requests.auth import HTTPBasicAuth

MAX = 3
# index name example: myIndex-2020.11.10
INDEX_POSTFIX = 'myIndex'
USER = os.environ.get('ES_USER')
PASSWD = os.environ.get('ES_PASSWORD')

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

def remove_index(index):
    resp = requests.delete(f'http://localhost:9200/{index}', auth=HTTPBasicAuth(USER, PASSWD))
    if resp.status_code == 200:
        log.info(f'index: {index} deleted')
    else:
        log.warn(f'code:{response.status_code} text:{response.text}')

def find_indexes_sorted():
    txt = requests.get(f'http://localhost:9200/_cat/indices/{INDEX_POSTFIX}*?h=index', auth=HTTPBasicAuth(USER, PASSWD))
    return sorted(txt.text.splitlines(), key=lambda item: datetime.datetime.strptime(item, f'{INDEX_POSTFIX}-%Y.%m.%d'))

def verify_state():
    if not USER or not PASSWD:
        raise Exception('missing environment: ES_USER / ES_PASSWORD')


verify_state()
done = False
deletes = 0
while not done:
    idx = find_indexes_sorted()
    if len(idx) > MAX:
        remove_index(idx[0])
        deletes += 1
        if deletes > 10:
            done = True
    else:
        done = True

if deletes == 0:
  log.info('nothing to do...')

