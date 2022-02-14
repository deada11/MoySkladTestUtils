"""
1. Добавить выбор файла (только json) с диска.
    1.1. Возможно добавить возможность скачивать файл по ссылке.
    1.2. Разобраться с тем, как подкладывать сертификаты в этом случае.
2. Добавить выбор параметров, которые надо засовывать в разобранный JSON - хотя зачем это вообще надо?
3. Добавить возможность сохранять распарсенный JSON в новый файл на диск.

5. Возможно, обернуть все в функции
"""
import json
import codecs
import re

file_name = 'Correct_test.json'

file = codecs.open(file_name, 'r', "utf_8_sig")
data = file.read()
created_pattern = r'"created":'
updated_pattern = r'"updated":'

print("Number of \"created\":", len(re.findall(created_pattern, data)))
print("Number of \"updated\":", len(re.findall(updated_pattern, data)))
file.close()

try:
    with open(file_name, 'r') as file:
        json_data = json.load(file)
        to_json = []
        for section in json_data.items():
            for i in range(len(section[1])):
                to_json.append({"id": section[1][i].get("id"),
                                "created": section[1][i].get("created"),
                                "updated": section[1][i].get("updated")})

    with open('parsed.json', 'w') as parsed:
        json.dump(to_json, parsed, sort_keys=False, indent=2)
        print("Успешно записано в файл 'parsed.json'")

except UnicodeDecodeError:
    print("В файле содержатся недопустимые символы.")
