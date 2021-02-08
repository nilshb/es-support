import requests
from requests.auth import HTTPBasicAuth
import time
import os

api_host = 'localhost:9200'
index_name = 'addresses'
user = os.environ.get('ES_USER')
password = os.environ.get('ES_PASSWORD')
file_name = '/Users/nhb/tmp/matrikkelenAdresse.csv'

count = 0
skip = 0
start = time.time()
bulk_doc = ''
opr = '{"index": {}}'


def index_doc(inxdoc):
    resp = requests.post(f'http://{api_host}/{index_name}/_bulk', data=inxdoc.encode('utf-8'),
                         headers={"Content-Type": "application/json; charset=utf-8"}, auth=HTTPBasicAuth(user, password))

    if resp.status_code != 200:
        print(str(resp.status_code) + ' ' + resp.text)


with open(file_name, 'r') as f:
    next(f)
    for line in f:
        line = line.strip()
        linesplit = line.split(';')
        gate = linesplit[7]
        nummer = linesplit[8] + linesplit[9]
        postnr = linesplit[19]
        poststed = linesplit[20].capitalize()
        if len(gate) > 1:
            doc = f"{{\"address\": \"{gate} {nummer}, {postnr} {poststed}\"}}"
            bulk_doc += (opr + '\n' + doc + '\n')
            count += 1
        else:
            skip += 1

        if count > 0 and count % 50000 == 0:
            index_doc(bulk_doc)
            bulk_doc = ''
            print(f'indexed: {count}, skipped: {skip}')


if len(bulk_doc) > 1:
    index_doc(bulk_doc)

print('-----------------------------------------------------------------')
print('docs indexed: ' + str(count))
print('docs skipped: ' + str(skip))
print('elapsed time: ' + str(time.time() - start) + 's')
