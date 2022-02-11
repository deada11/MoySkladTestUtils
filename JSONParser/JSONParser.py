"""
1. Добавить выбор файла (только json) с диска.
    1.1. Возможно добавить возможность скачивать файл по ссылке.
    1.2. Разобраться с тем, как подкладывать сертификаты в этом случае.
2. Добавить выбор параметров, которые надо засовывать в разобранный JSON - хотя зачем это вообще надо?
3. Добавить возможность сохранять распарсенный JSON в новый файл на диск.
"""
import json

with open('ExportAccountRequest.json', 'r') as file:
    json_data = json.load(file)

to_json = []
for section in json_data.items():
    for i in range(len(section[1])):
        to_json.append({"id": section[1][i].get("id"),
                        "created": section[1][i].get("created"),
                        "updated": section[1][i].get("updated")})

t = open('parsed.json', 'w')
json.dump(to_json, t, sort_keys=False, indent=2)
t.close()
