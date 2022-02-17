"""
1. Добавить выбор файла (только json) с диска.
    1.1. Возможно добавить возможность скачивать файл по ссылке.
    1.2. Разобраться с тем, как подкладывать сертификаты в этом случае.
2. Добавить выбор параметров, которые надо засовывать в разобранный JSON - хотя зачем это вообще надо?
3. Добавить возможность сохранять распарсенный JSON в новый файл на диск.
4. Даты привести в нормальный вид
5. Придумать, как выводить минимальные и максимальные значения created & updated без создания доп сущностей
"""
import json
import re
import datetime


def decorator(func):
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        print('__________________________________________')

    return wrap


def Create_parsed_list(json_for_parse, to_json=[]):
    for section in json_for_parse.items():
        for i in range(len(section[1])):
            to_json.append(
                dict(id=section[1][i].get("id"), created=section[1][i].get("created"),
                     updated=section[1][i].get("updated"), partnerId=section[1][i].get("partnerId"),
                     partnerCode=section[1][i].get("partnerCode"))
            )
    return to_json


@decorator
def Min_max_values(json_for_parse):
    created_list = []
    updated_list = []
    for element in Create_parsed_list(json_for_parse):
        created_list.append(element.get("created"))
        updated_list.append(element.get("updated"))
    print("Minimum created date:", min(created_list))
    print("Maximum created date:", max(created_list))
    print("Minimum updated date:", min(updated_list))
    print("Maximum updated date:", max(updated_list))


@decorator
def Counting(string_for_count):
    print("Number of \"created\":", len(re.findall(created_pattern, str(string_for_count))))
    print("Number of \"updated\":", len(re.findall(updated_pattern, str(string_for_count))))
    print("Number of not null \"partnerId\":", len(re.findall(partnerId_pattern, str(string_for_count))))
    print("Number of not null \"partnerCode\":", len(re.findall(partnerCode_pattern, str(string_for_count))))


created_pattern = r'created'
updated_pattern = r'updated'
partnerId_pattern = r'partnerId'
partnerCode_pattern = r'partnerCode'

file_name = 'ExportAccountRequest.json'

try:
    with open(file_name, 'r', encoding="utf-8") as file:
        json_data = json.load(file)
        Min_max_values(json_data)
        Counting(json_data)

    with open('parsed.json', 'w') as parsed:
        json.dump(Create_parsed_list(json_data), parsed, sort_keys=False, indent=2, ensure_ascii=False)
        print("Успешно записано в файл 'parsed.json'")

except UnicodeDecodeError:
    print("В файле содержатся недопустимые символы.")
