from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Size = namedtuple('Size', ['width', 'height'])
Keypoint = namedtuple('Keypoint', ['x', 'y', 'v'])
BoundingBox = namedtuple('BoundingBox', ['xmin', 'ymin', 'xmax', 'ymax'])