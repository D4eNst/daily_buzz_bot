import yaml

with open('data/messages.yaml', encoding='utf-8') as stream:
    messages = yaml.load(stream, Loader=yaml.FullLoader)
with open('data/buttons.yaml', encoding='utf-8') as stream:
    buttons = yaml.load(stream, Loader=yaml.FullLoader)