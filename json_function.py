import json


class JsonConnector:
    def __init__(self):
        ...
        
    def info_in_json(self, key, value):
        with open('CONSTANT.json', 'r') as f:
            str_info = " ".join(value)
            info = json.loads(f.read())
            info[key] = str_info
            ...
        with open('CONSTANT.json', 'w') as f:
            f.write(json.dumps(info))
        
    def info_from_json(self):
        with open('CONSTANT.json', 'r') as f:
            str_info = ''
            info = json.loads(f.read())
            for key, value in info.items():
                str_info = str_info + f'{key}: {value}\n\n'
        return str_info

    
    def get_constains(self, key):
        with open('CONSTANT.json', 'r') as f:
            info = json.loads(f.read())
        return info[key]