'''
Создание нужного количества доп. полей типа Строка
'''

import json
from getpass import getpass
import requests
from requests.auth import HTTPBasicAuth

n = input('Онлайн: ')
acc = input('Аккаунт: ')
passw = getpass()
fields = input('Сколько доп. полей нужно? ')

big_data = []
for i in range(int(fields)):
    data = {}
    data["name"] = "Строковое {}".format(str(i))
    data["type"] = "string"
    big_data.append(data)

url_attributes = 'https://online-{}.testms.lognex.ru/api/remap/1.2/entity/product/metadata/attributes/'.format(n)
my_headers = {'Content-type': 'application/json'}

response_attr = requests.post(url_attributes,
                              headers = my_headers,
                              auth = HTTPBasicAuth(acc, passw),
                              data = json.dumps(big_data))

print('status', response_attr)
json_response_attr = response_attr.json()

if str(response_attr) != '<Response [200]>':
    print(json_response_attr[0]['errors'][0]['error'])
    print('')

while True:
    x = input('Для выхода нажмите Enter')
    if x=='':
        break
