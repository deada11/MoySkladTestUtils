'''
Создание выбранного числа модификаций у одного товара
'''

import json
import math
from getpass import getpass
import requests
from requests.auth import HTTPBasicAuth

n = input('Онлайн: ')
acc = input('Аккаунт: ')
passw = getpass()
print('Будет создан товар "Мандарины" и модификации к нему.')
variants = input('Сколько модификаций создать? ')

url = 'https://online-{}.testms.lognex.ru/api/remap/1.2/entity/product'.format(n)
data = {}
data["name"]="Мандарины"
response_product = requests.post(url,
                                 headers={'Content-Type':'application/json'},
                                 auth=HTTPBasicAuth(acc, passw),
                                 data = json.dumps(data))

json_response_product = response_product.json()
print(response_product.status_code)
print('Создан товар ', json_response_product['name'], ' с id ', json_response_product['id'])
created_id = json_response_product['id']
product = json_response_product['meta']
url_var = 'https://online-{}.testms.lognex.ru/api/remap/1.2/entity/variant'.format(n)

count = math.ceil(int(variants)/1000)

print('Создаем модификации массово. Потребуется запросов: ', count)
var_data_big = []

for i in range(int(variants)):
    var_data= {}
    var_data['name'] = '(желтый{})'.format(i)
    var_data['characteristics'] = [{'name': 'цвет', 'value':'желтый{}'.format(i)}]
    var_data['product'] = {'meta':product}
    var_data_big.append(var_data)

for i in range(count):
    try:
        data = var_data_big[i*1000:i*1000+1000]
    except IndexError: 
        data = var_data_big[i*1000:len(var_data_big)-1]
    response_var = requests.post(url_var,
                                 headers={'Content-Type':'application/json'},
                                 auth=HTTPBasicAuth(acc, passw),
                                 data = json.dumps(data))
    print('status ', response_var)
    json_response_var = response_var.json()
    if str(response_var) != '<Response [200]>':
        print(json_response_var[0]['errors'][0]['error'])
        print('')

while True:
    x = input('Для выхода нажмите Enter')
    if x=='':
        break
