def parse_str_from_tag(text: str, tag: str) -> str:
    return text.split(f'<{tag}>')[1].split(f'</{tag}>')[0]

def parse_int_from_tag(text: str, tag: str) -> int:
    return int(parse_str_from_tag(text, tag))