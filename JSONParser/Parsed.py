import json
with open('parsed.json', 'r') as file:
    data = json.load(file)
    yclid = 0
    undefined_yclid = 0
    for element in data:
        if element.get("yclid") != [] and element.get("yclid") != ["undefined"]:
            yclid += 1
        if element.get("yclid") == ["undefined"]:
            undefined_yclid += 1

file.close()
print(yclid, undefined_yclid,
      yclid + undefined_yclid)
