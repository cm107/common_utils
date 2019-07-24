def parse_str_from_tag(text: str, tag: str) -> str:
    return text.split(f'<{tag}>')[1].split(f'</{tag}>')[0]

def parse_int_from_tag(text: str, tag: str) -> int:
    return int(parse_str_from_tag(text, tag))

def str2strlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').replace("'", "").split(',')
    return [i for i in temp]

def str2intlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').split(',')
    return [int(i) for i in temp]

def str2floatlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').split(',')
    return [float(i) for i in temp]

def str2bool(text_str: str) -> bool:
    if text_str.lower() == 'true':
        return True
    elif text_str.lower() == 'false':
        return False
    else:
        raise Exception(f"{text_str} cannot be converted to bool")