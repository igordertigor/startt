import os
import json

def config(path):
    filename = os.path.join(path, 'config.json')
    if os.path.exists(filename):
        with open(filename) as f:
            out = json.load(f)
            out.setdefault('default', 'link')
            return out
    else:
        return {'default': 'link'}
