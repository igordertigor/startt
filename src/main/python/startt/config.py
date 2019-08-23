import os
import json


def config(path):
    filename = os.path.join(path, 'config.json')
    if os.path.exists(filename):
        with open(filename) as f:
            out = json.load(f)
        if not set(out.values()).issubset({'link', 'copy'}):
            raise ValueError('Invalid transfer option in config: {}'
                             .format(set(out.values()) - {'link', 'copy'})
                             )
        out.setdefault('default', 'link')
        return out
    else:
        return {'default': 'link'}
