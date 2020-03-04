import time
from logger import logger
from common_utils.path_utils import find_longest_container_dir

path_list = [
    '/path/to/dir/a/b/c/d.png',
    '/path/to/dir/a/temp/example.png',
    '/path/to/dir/a/b/example0.png',
    '/path/to/dir/a/z/x.png'
]
time0 = time.time_ns()
result = find_longest_container_dir(path_list)
time1 = time.time_ns()
assert result == '/path/to/dir/a'
logger.cyan(result)
logger.purple(f'{time1-time0} ns ellapsed')