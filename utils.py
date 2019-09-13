import numpy as np
import json

def str2bool(text_str: str) -> bool:
    if text_str.lower() == 'true':
        return True
    elif text_str.lower() == 'false':
        return False
    else:
        raise Exception(f"{text_str} cannot be converted to bool")

def parse_str_from_tag(text: str, tag: str) -> str:
    return text.split(f'<{tag}>')[1].split(f'</{tag}>')[0]

def parse_int_from_tag(text: str, tag: str) -> int:
    return int(parse_str_from_tag(text, tag))

def remove_leftmost_squarebracket_from_str(text: str) -> str:
    return '['.join(text.split('[')[1:])

def remove_rightmost_squarebracket_from_str(text: str) -> str:
    return ']'.join(text.split(']')[:-1])

def remove_edge_squarebrackets_from_str(text: str) -> str:
    temp = remove_leftmost_squarebracket_from_str(text)
    temp = remove_rightmost_squarebracket_from_str(temp)
    return temp

def get_str_lists_from_noedge_str(text: str) -> str:
    list_chunks = [j.replace(']', '') for j in [i.replace(' ', '') for i in ''.join(text.split('[')).split('],')]]
    return [list_chunk.split(',') for list_chunk in list_chunks]

def str2strlistlist(list_str: str) -> list:
    no_edges = remove_edge_squarebrackets_from_str(list_str)
    return get_str_lists_from_noedge_str(no_edges)

def strlist2intlist(strlist: list) -> list:
    list_buffer = []
    for str_text in strlist:
        list_buffer.append(int(str_text))
    return list_buffer

def strlist2floatlist(strlist: list) -> list:
    list_buffer = []
    for str_text in strlist:
        list_buffer.append(float(str_text))
    return list_buffer

def strlist2boollist(strlist: list) -> list:
    list_buffer = []
    for str_text in strlist:
        list_buffer.append(str2bool(str_text))
    return list_buffer

def strlistlist2intlistlist(strlistlist: list) -> list:
    list_buffer = []
    for strlist in strlistlist:
        list_buffer.append(strlist2intlist(strlist))
    return list_buffer

def strlistlist2floatlistlist(strlistlist: list) -> list:
    list_buffer = []
    for strlist in strlistlist:
        list_buffer.append(strlist2floatlist(strlist))
    return list_buffer

def strlistlist2boollistlist(strlistlist: list) -> list:
    list_buffer = []
    for strlist in strlistlist:
        list_buffer.append(strlist2boollist(strlist))
    return list_buffer

def str2intlistlist(text: str) -> list:
    return strlistlist2intlistlist(str2strlistlist(text))

def str2floatlistlist(text: str) -> list:
    return strlistlist2floatlistlist(str2strlistlist(text))

def str2boollistlist(text: str) -> list:
    return strlistlist2boollistlist(str2strlistlist(text))

def str2strlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').replace("'", "").split(',')
    return [i for i in temp]

def str2intlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').split(',')
    return [int(i) for i in temp]

def str2floatlist(list_str: str) -> list:
    temp = list_str.split('[')[1].split(']')[0].replace(' ', '').split(',')
    return [float(i) for i in temp]

def get_list_dimension(list_data: list) -> int:
    return len(np.array(list_data).shape)

def beautify_dict(data: dict, indent: int=2):
    return json.dumps(data, indent=indent)

def list1d2chunks(data_list: list, chunk_size: int):
    if len(data_list) % chunk_size != 0:
        raise Exception(f"len(data_list) % chunk_size != 0 -> {len(data_list)} % {chunk_size} != 0 -> {len(data_list) % chunk_size} != 0")
    return np.array(data_list).reshape(-1, chunk_size).tolist()

def chunks2list1d(chunks: list):
    return np.array(chunks).reshape(-1).tolist()

def rshift(val_list: list, shift_by: int) -> list:
    i = shift_by % len(val_list)
    return val_list[-i:] + val_list[:-i]

def lshift(val_list: list, shift_by: int) -> list:
    i = shift_by % len(val_list)
    return val_list[i:] + val_list[:i]