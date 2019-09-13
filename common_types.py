from collections import namedtuple
from ..logger.logger_handler import logger
from .check_utils import check_type_from_list, check_list_length

Keypoint = namedtuple('Keypoint', ['x', 'y', 'v'])
BoundingBox = namedtuple('BoundingBox', ['xmin', 'ymin', 'xmax', 'ymax'])

class Point:
    def __init__(self, x, y, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[x, y], valid_type_list=[int, float])
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point: (x, y)=({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def to_int(self):
        return Point(x=int(self.x), y=int(self.y), check_types=False)

    def to_float(self):
        return Point(x=float(self.x), y=float(self.y), check_types=False)

    def to_labelme_format(self):
        return [[self.x, self.y]]

    def items(self) -> list:
        return [self.x, self.y]

    def to_list(self) -> list:
        return [self.x, self.y]

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def types(self) -> list:
        return [type(self.x), type(self.y)]

    @classmethod
    def from_list(self, items: list):
        check_list_length(item_list=items, correct_length=2)
        return Point(x=items[0], y=items[1])

    @classmethod
    def from_labelme_point_list(self, labelme_point_list: list):
        check_list_length(item_list=labelme_point_list, correct_length=1)
        [[x, y]] = labelme_point_list
        return Point(x, y)

class Rectangle:
    def __init__(self, xmin, ymin, xmax, ymax, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[xmin, xmax, ymin, ymax], valid_type_list=[int, float])
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.width = xmax - xmin
        self.height = ymax - ymin
        self.p0 = Point(x=xmin, y=ymin)
        self.p1 = Point(x=xmax, y=ymax)
        self.area = self.width * self.height
        self.point_list = [self.p0, self.p1]

    def __str__(self):
        return f"Rectangle: (xmin, ymin, xmax, ymax)=({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"

    def __repr__(self):
        return self.__str__()

    def to_int(self):
        return Rectangle(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax),
            check_types=False
        )

    def to_float(self):
        return Rectangle(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax),
            check_types=False
        )

    def to_coco_format(self):
        return [self.xmin, self.ymin, self.width, self.height]

    def to_labelme_format(self) -> list:
        return [[self.xmin, self.ymin], [self.xmax, self.ymax]]

    @classmethod
    def from_p0p1(self, p0: Point, p1: Point) -> Point:
        return Rectangle(xmin=p0.x, ymin=p0.y, xmax=p1.x, ymax=p1.y, check_types=False)

    @classmethod
    def from_labelme_point_list(self, labelme_point_list: list):
        check_list_length(item_list=labelme_point_list, correct_length=2)
        [[xmin, ymin], [xmax, ymax]] = labelme_point_list
        return Rectangle(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

class Polygon:
    def __init__(self, point_list: list):
        check_type_from_list(item_list=point_list, valid_type_list=[Point])
        self.point_list = point_list
        self.rectangle = self._get_rectangle()
        self.rectangle_area = self.rectangle.area

    def _get_rectangle(self) -> Rectangle:
        xmin, ymin = self.point_list[0].x, self.point_list[0].y
        xmax, ymax = self.point_list[0].x, self.point_list[0].y
        for point in self.point_list[1:]:
            if point.x < xmin:
                xmin = point.x
            elif point.x > xmax:
                xmax = point.x
            if point.y < ymin:
                ymin = point.y
            elif point.y > ymax:
                ymax = point.y
        return Rectangle(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def to_labelme_format(self):
        return [[point.x, point.y] for point in self.point_list]

    @classmethod
    def from_labelme_point_list(self, labelme_point_list: list):
        return Polygon([Point(x=item[0], y=item[1]) for item in labelme_point_list])

class Size:
    _from_list_length = 2
    def __init__(self, width, height, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[width, height], valid_type_list=[int, float])
        self.width = width
        self.height = height
        self.area = width * height

    def __str__(self):
        return f"Size: (width, height)=({self.width},{self.height})"

    def __repr__(self):
        return self.__str__()

    def to_int(self):
        return Size(width=int(self.width), height=int(self.height), check_types=False)

    def to_float(self):
        return Size(width=float(self.width), height=float(self.height), check_types=False)

    def to_list(self):
        return [self.width, self.height]

    def items(self) -> list:
        return [self.width, self.height]

    def types(self):
        return [type(self.width), type(self.height)]

    @classmethod
    def from_list(self, items: list):
        check_list_length(item_list=items, correct_length=self._from_list_length)
        return Size(width=items[0], height=items[1])

    @classmethod
    def from_cv2_shape(self, cv2_shape: list):
        h, w = cv2_shape[:2]
        return Size(width=w, height=h)

class Resize:
    def __init__(self, old_size: Size, new_size: Size):
        self.old_size = old_size
        self.new_size = new_size
        self.w_resize_factor = new_size.width / old_size.width
        self.h_resize_factor = new_size.height / old_size.height

    def on_point(self, point: Point) -> Point:
        return Point(x=point.x*self.w_resize_factor, y=point.y*self.h_resize_factor)

    def on_rectangle(self, rectangle: Rectangle) -> Rectangle:
        p0, p1 = self.on_point(rectangle.p0), self.on_point(rectangle.p1)
        return Rectangle.from_p0p1(p0, p1)

    def on_polygon(self, polygon: Polygon) -> Polygon:
        return Polygon([self.on_point(point) for point in polygon.point_list])
