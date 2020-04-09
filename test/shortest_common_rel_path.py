import time
from logger import logger
from common_utils.path_utils import find_shortest_common_rel_path

path_list = [
    '/path/to/dir/a/b/c/d.png',
    'path/lskdjf/to/dir/a/b/c/d.png',
    'path/to/a/dir/a/b/c/d.png',
    'lksjdfljksdlkfjlsdkfj/c/d.png'
]
time0 = time.time_ns()
result = find_shortest_common_rel_path(path_list)
time1 = time.time_ns()
assert result == 'c/d.png'
logger.cyan(result)
logger.purple(f'{time1-time0} ns ellapsed')