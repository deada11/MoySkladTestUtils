"""
Удаление всего ассортимента (в том числе в архиве) из всех групп товаров на аккаунте.
Используются запросы к REMAP 1.2 на получение meta-данных
в json-формате и массовое удаление сущностей
"""
import json
import math
from getpass import getpass
import requests
from requests.auth import HTTPBasicAuth

n = input('Неймспейс: ')
acc = input('Аккаунт: ')
passw = getpass()


def do_get(entity):
    """
    Функция, которая запрашивает информацию о выбранном типе сущностей на аккаунте

    Parameters:
        entity (str): Выбраный тип сущности.
        Поддерживаются типы, описанные в документации на REMAP 1.2

    Returns:
        Кортеж из 3 элементов: (entities_meta, count, size)
        entities_meta ([{json_interpretation}]): Список мета-данных по каждой сущности выбранного типа
        count (int): Количество страниц в выводе ответа. Каждая содержит по 1000 элементов
        size (int): Количество сущносей выранного типа на аккаунте
    """
    print('Получаем список сущностей... ', entity)
    url = f'https://online-{n}.testms-test.lognex.ru/api/remap/1.2/entity/{entity}?filter=archived=true;archived=false'
    response = requests.get(url,
                            headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth(acc, passw))
    if str(response) == '<Response [412]>':
        url = f'https://online-{n}.testms-test.lognex.ru/api/remap/1.2/entity/{entity}'
        response = requests.get(url,
                                headers={'Content-Type': 'application/json'},
                                auth=HTTPBasicAuth(acc, passw))
    print(' status ', response)
    print('')
    json_response = response.json()
    size = json_response['meta']['size']
    limit = json_response['meta']['limit']
    print('Сущностей на аккаунте: ', size)

    count = math.ceil(size / 1000)
    entities_meta = []

    for i in range(count):
        offset = 1000 * i
        url = f'https://online-{n}.testms-test.lognex.ru/api/remap/1.2/entity/{entity}' \
              f'?filter=archived=true;archived=false&limit={limit}&offset={offset}'
        response = requests.get(url,
                                headers={'Content-Type': 'application/json'},
                                auth=HTTPBasicAuth(acc, passw))
        if str(response) == '<Response [412]>':
            url = f'https://online-{n}.testms-test.lognex.ru/api/remap/1.2/entity/{entity}'
            response = requests.get(url,
                                    headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth(acc, passw))
        json_response = response.json()
        if str(response) != '<Response [200]>':
            print(json_response[0]['errors'][0]['error'])
        for j in json_response['rows']:
            temp = {'meta': j['meta']}
            entities_meta.append(temp)
    return entities_meta, count, size


def do_delete(entity):
    """
    Функция, которая удаляет все выбранные сущности на аккаунте.

    Parameters:
        entity (str): Выбраный тип сущности. Поддерживаются типы, описанные в документации на REMAP 1.2
    """
    entity_tuple = do_get(entity)
    data_big = entity_tuple[0]
    count_del = entity_tuple[1]
    print('Удаляем массово. Потребуется запросов: ', count_del)
    data = []
    for i in range(count_del):
        try:
            data = data_big[i * 1000:i * 1000 + 1000]
        except IndexError:
            data = data_big[i * 1000:len(entity_tuple[0]) - 1]
        url = 'https://online-{}.testms-test.lognex.ru/api/remap/1.2/entity/{}/delete'.format(n, entity)
        response_del = requests.post(url,
                                     headers={'Content-Type': 'application/json'},
                                     auth=HTTPBasicAuth(acc, passw),
                                     data=json.dumps(data))
        print(' status ', response_del)
        json_response_del = response_del.json()
        if (str(response_del) != '<Response [200]>') and (entity != 'productfolder'):
            print('    ', json_response_del[0]['errors'][0]['error'])
        print('')


'''
Основное выполнение программы.
1. Запрос документов на аккаунте
'''
ops = do_get('operation')
x = 'n'

'''
Если документы есть, то по решению пользователя удаляются все документы по типам.
После удаления каждого типа документов опять происходит запрос всех документов,
до тех пор, пока в ответе не будет 0.
'''
if ops[2] != 0:
    print('На аккаунте есть документы, в которых могут быть задействованы товары.')
    while True:
        x = input('Удалять документы? y/n: ')
        if x in ('y', 'n'):
            break
if x == 'y':
    while ops[2] != 0:
        current_doc = ops[0][0]['meta']['type']
        do_delete(current_doc)
        ops = do_get('operation')
print('---------------------------')

'''
2. Удаление всего ассортимента
'''
do_delete('assortment')
print('---------------------------')
while True:
    x = input('Удалять группы товаров? y/n: ')
    if x in ('y', 'n'):
        break

'''
3. Удаление всех групп товаров по решению пользователя
'''
if x == 'y':
    do_delete('productfolder')

while True:
    x = input('Для выхода нажмите Enter')
    if x == '':
        break
