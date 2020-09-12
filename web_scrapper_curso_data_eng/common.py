# Necesita el archivo config.yaml para cargar en __config el diccionario en formato yaml
# Donde se definieron las fuentes de información, existen otros formatos como json

import yaml

__config = None

def config():
    global __config
    if not __config:
        with open('config.yaml', mode='r') as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)

    return __config