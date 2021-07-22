import json

with open('final_data.json') as f:
  data = json.load(f)

for key in data:
    
    inner = "".join(s for s in data.get(key))
    d = {
        "_id": "auto:0",
        "toplevel_": True,
        "name": key + " " + inner,
        "attributes": [{ "property": k, "value": v } for k, v in data.get(key).get(inner).get("data").items() ]
    }

    c = {
        "_id": "auto:1",
        "array": [
            {"property": "Element"},
            {"property": "Min"},
            {"property": "Max"}
        ],
        "value": [ [d.get("0"), d.get("1"), d.get("2")] for d in data.get(key).get(inner).get("analysis") if d.get("0") != "Element" and (d.get("1") != "" or d.get("2") != "") ],
        "valuetype": "array",
        "sectags": ["Analysis"],
    }

    print(c)
    break