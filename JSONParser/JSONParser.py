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
