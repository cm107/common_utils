import numpy as np

def parse_str_from_tag(text: str, tag: str) -> str:
    return text.split(f'<{tag}>')[1].split(f'</{tag}>')[0]

def parse_int_from_tag(text: str, tag: str) -> int:
    return int(parse_str_from_tag(text, tag))

def str2intlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').split(',')
    return [int(i) for i in temp]

def get_list_dimension(list_data: list) -> int:
    return len(np.array(list_data).shape)