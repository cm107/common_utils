from logger import logger
from ..file_utils import file_exists, dir_exists
from ..path_utils import get_dirpath_from_filepath

def check_type(item, valid_type_list: list):
    if type(item) not in valid_type_list:
        logger.error(f"Invalid type: {type(item)}")
        logger.error(f"Valid types: {valid_type_list}")
        raise TypeError

def check_type_from_list(item_list: list, valid_type_list: list):
    for item in item_list:
        check_type(item=item, valid_type_list=valid_type_list)

def check_value(item, valid_value_list: list):
    if item not in valid_value_list:
        logger.error(f"Invalid value: {item}")
        logger.error(f"Valid values: {valid_value_list}")
        raise TypeError

def check_value_from_list(item_list: list, valid_value_list: list):
    for item in item_list:
        check_value(item=item, valid_value_list=valid_value_list)

def check_file_exists(filepath: str):
    if not file_exists(filepath):
        logger.error(f"File not found: {filepath}")
        raise Exception

def check_filepath_list_exists(filepath_list: list):
    for filepath in filepath_list:
        check_type(item=filepath, valid_type_list=[str])
        check_file_exists(filepath=filepath)

def check_dir_exists(dirpath: str):
    if not dir_exists(dirpath):
        logger.error(f"Directory not found: {dirpath}")
        raise Exception

def check_dirpath_list_exists(dirpath_list: list):
    for dirpath in dirpath_list:
        check_type(item=dirpath, valid_type_list=[str])
        check_dir_exists(dirpath=dirpath)

def check_input_path_and_output_dir(input_path: str, output_path: str):
    check_file_exists(filepath=input_path)
    output_dir = get_dirpath_from_filepath(filepath=output_path)
    check_dir_exists(dirpath=output_dir)

def check_list_length(item_list: list, correct_length: int, ineq_type: str='eq'):
    list_length = len(item_list)
    if ineq_type.lower() in ['eq', 'equal', 'e', 'equal_to', 'et']:
        if not list_length == correct_length:
            logger.error(f"Expected list length == {correct_length}. Encountered {list_length}")
            raise Exception
    elif ineq_type.lower() in ['gt', 'greater', 'g', 'greater_than']:
        if not list_length > correct_length:
            logger.error(f"Expected list length > {correct_length}. Encountered {list_length}")
            raise Exception
    elif ineq_type.lower() in ['lt', 'less', 'l', 'less_than']:
        if not list_length < correct_length:
            logger.error(f"Expected list length < {correct_length}. Encountered {list_length}")
            raise Exception
    elif ineq_type.lower() in ['ge', 'greater_than_or_equal_to']:
        if not list_length >= correct_length:
            logger.error(f"Expected list length >= {correct_length}. Encountered {list_length}")
            raise Exception
    elif ineq_type.lower() in ['le', 'less_than_or_equal_to']:
        if not list_length <= correct_length:
            logger.error(f"Expected list length <= {correct_length}. Encountered {list_length}")
            raise Exception
    else:
        logger.error(f"Invalid ineq_type: {ineq_type}")
        raise Exception

def check_key_in_dict(item_dict: dict, key):
    if key not in item_dict:
        logger.error(f"Key {key} not found in dictionary.")
        raise Exception

def check_key_not_in_dict(item_dict: dict, key):
    if key in item_dict:
        logger.error(f"Key {key} already exists in dictionary.")
        raise Exception