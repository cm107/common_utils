import operator

def count_list_items(item_list: list) -> list:
    possibilities = {}
    for item in item_list:
        if item not in possibilities:
            possibilities[item] = 1
        else:
            possibilities[item] = possibilities[item] + 1
    
    ordered_list = sorted(possibilities.items(), key=operator.itemgetter(1), reverse=True)
    return ordered_list