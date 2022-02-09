'''
Перенос всех товаров на аккаунте в архив или извлечение из архива.
'''

import json
import math
from getpass import getpass
import requests
from requests.auth import HTTPBasicAuth

while True:
    choice = input('Если хотите перенести все товары в архив, нажмите 1. Если извлечь, - нажмите 2: ')
    if choice in('1', '2'):
        break

archived = True

if choice == '2':
    archived = False

n = input('Неймспейс: ')
acc = input('Аккаунт: ')
passw = getpass()

good_id = []
url = 'https://online-{}.testms.lognex.ru/api/remap/1.2/entity/product?filter=archived=true;archived=false'.format(n)
response = requests.get(url,
                        headers = {'Content-Type':'application/json'},
                        auth=HTTPBasicAuth(acc, passw))
print('Получаем товары...')
print('status ', response)
json_response = response.json()
size = json_response['meta']['size']
limit = json_response['meta']['limit']
print('Товаров на аккаунте: ', size)

count = math.ceil(size/1000)
goods = []
goods_id = []
print('Страниц в выводе ответа: ', count)
print('')

for i in range(count):
    print('Сохраняем страницу ', i+1)
    offset = 1000*i
    url = 'https://online-{}.testms.lognex.ru/api/remap/1.2/entity/product?filter=archived=true;archived=false&limit={}&offset={}'.format(n, limit, offset)
    response = requests.get(url,
                            headers = {'Content-Type':'application/json'},
                            auth=HTTPBasicAuth(acc, passw))
    json_response = response.json()
    if str(response) != '<Response [200]>':
        print(json_response[0]['errors'][0]['error'])
    for j in json_response['rows']:
        temp = {'id':j['id'], 'archived': archived}
        goods_id.append(temp)
count_del = count

if archived:
    print('Отправляем в архив массово. Потребуется запросов: ', count_del)
else:
    print('Извлекаем из архива массово. Потребуется запросов: ', count_del)

data = []
for i in range(count_del):
    try:
        data = goods_id[i*1000:i*1000+1000]
    except IndexError:
        data = goods_id[i*1000:len(goods_id)-1]
    url = 'https://online-{}.testms.lognex.ru/api/remap/1.2/entity/product'.format(n)
    response_archive = requests.post(url,
                                headers = {'Content-Type':'application/json'},
                                auth=HTTPBasicAuth(acc, passw),
                                data = json.dumps(data))
    print('status ', response_archive)
    json_response_archive = response_archive.json()
    if str(response_archive) != '<Response [200]>':
        print(json_response_archive[0]['errors'][0]['error'])
    print('')

while True:
    x = input('Для выхода нажмите Enter')
    if x=='':
        break
