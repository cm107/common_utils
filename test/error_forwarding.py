from logger import logger
from common_utils.error_utils.decorators import bypass_error_in_func, bypass_error_in_classmethod

def test_func_a():
    raise Exception

def test_func_b():
    test_func_a()

def test_func_c():
    test_func_b()

logger.info(f'Function Test')

@bypass_error_in_func(logger.error)
def test_func_d():
    test_func_c()

def test():
    test_func_d()
    logger.good(f'Success!')

for i in range(3):
    print(f'i: {i}')
    test()

logger.info(f'Class Test')

class TestObj:
    def __init__(self):
        pass

    @bypass_error_in_classmethod(logger.error)
    def method_a(self):
        test_func_c()
    
    @classmethod
    @bypass_error_in_classmethod(logger.error)
    def classmethod_a(cls):
        test_func_c()

test_obj = TestObj()
test_obj.method_a()
logger.good('Success!')

TestObj.classmethod_a()
logger.good('Success!')