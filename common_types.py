from collections import namedtuple
from ..logger.logger_handler import logger
from .check_utils import check_type_from_list, check_list_length
from math import pi, asin, tan

Keypoint = namedtuple('Keypoint', ['x', 'y', 'v'])
BoundingBox = namedtuple('BoundingBox', ['xmin', 'ymin', 'xmax', 'ymax'])

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
    def from_p0size(self, p0: Point, size: Size):
        return Rectangle(xmin=p0.x, ymin=p0.y, xmax=(p0.x + size.width), ymax=(p0.y + size.height))

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

class Circle:
    def __init__(self, center: Point, radius, check_types: bool=True):
        if check_types:
            check_type_from_list(item_list=[radius], valid_type_list=[int, float])
        self.center = center
        self.radius = radius

    def __str__(self):
        return f"Center: ({self.center.x}, {self.center.y}), Radius: {self.radius}"

    def __repr__(self):
        return self.__str__()

class Ellipse:
    def __init__(self, center: Point, size: Size):
        self.center = center
        if size.width == size.height:
            logger.red(f"Invalid Dimensions: size.width == size.height -> {size.width} == {size.height}")
            logger.red(f"You defined a circle. Please use Circle instead.")
            raise Exception
        self.size = size
        self.rectangle = Rectangle(
            xmin=self.center.x-(self.size.width/2),
            ymin=self.center.y-(self.size.height/2),
            xmax=self.center.x+(self.size.width/2),
            ymax=self.center.y+(self.size.height/2)
        )

        self.a = size.width / 2
        self.b = size.height / 2
        self.major = 'x' if self.a > self.b else 'y'
        self.c = (self.a**2 - self.b**2)**0.5 if self.major == 'x' else (self.b**2 - self.a**2)**0.5
        self.e = self.c / self.a if self.major == 'x' else self.c / self.b
        
        self.foci = []
        self.directrix = []
        if self.major == 'x':
            self.foci.append(Point(x=self.center.x+self.c, y=self.center.y))
            self.foci.append(Point(x=self.center.x-self.c, y=self.center.y))
            self.directrix.append(center.x + (self.a / self.e))
            self.directrix.append(center.x - (self.a / self.e)) 
        else:
            self.foci.append(Point(x=self.center.x, y=self.center.y+self.c))
            self.foci.append(Point(x=self.center.x, y=self.center.y-self.c))
            self.directrix.append(center.y + (self.b / self.e))
            self.directrix.append(center.y - (self.b / self.e))

    def __str__(self):
        return f"Center: ({self.center.x}, {self.center.y}), Size: ({self.size.width}, {self.size.height})"

    def __repr__(self):
        return self.__str__()

    def get_equation_str(self, eval_square: bool=False):
        if not eval_square:
            return f'((x-{self.center.x})^2)/({self.a}^2) + ((y-{self.center.y})^2)/({self.b}^2) == 1' 
        else:
            return f'((x-{self.center.x})^2)/{self.a**2} + ((y-{self.center.y})^2)/{self.b**2} == 1'

    def get_area(self):
        return pi * self.a * self.b

    def get_points_given_val(self, given_var: str, given_val):
        solution = []
        if given_var == 'y':
            x_pos = self.center.x + self.a * (1 - (((given_val - self.center.y)**2)/((self.b)**2)))**0.5
            solution.append(Point(x=x_pos, y=given_val))
            x_neg = self.center.x - self.a * (1 - (((given_val - self.center.y)**2)/((self.b)**2)))**0.5
            solution.append(Point(x=x_neg, y=given_val))
        elif given_var == 'x':
            y_pos = self.center.y + self.b * (1 - (((given_val - self.center.x)**2)/((self.a)**2)))**0.5
            solution.append(Point(x=given_val, y=y_pos))
            y_neg = self.center.y - self.b * (1 - (((given_val - self.center.x)**2)/((self.a)**2)))**0.5
            solution.append(Point(x=given_val, y=y_neg))
        else:
            logger.error(f"Invalid given_var: {given_var}")
            logger.error(f"Valid given_var: {['x', 'y']}")
            raise Exception
        return solution

    def get_radius_and_points_given_val(self, given_var: str, given_val):
        points = self.get_points_given_val(given_var=given_var, given_val=given_val)
        point = points[0] # only need one
        radius = ((point.x - self.center.x)**2 + (point.y - self.center.y)**2)**0.5
        return radius, points

    # TODO: Fix this method
    # def get_radius_angle_and_points_given_val(self, given_var: str, given_val, use_deg: bool=True):
    #     radius, points = self.get_radius_and_points_given_val(given_var=given_var, given_val=given_val)
    #     angles = []
    #     if self.major == 'x':
    #         k = (self.b/(radius*self.c))*(self.a**2 + radius**2)**0.5
    #         k = 1.0 if k > 1.0 else 0.0 if k < 0.0 else k
    #         angles.append(asin(k))
    #         angles.append(asin(-k))
    #     elif self.major == 'y':
    #         k = (self.a/(radius*self.c))*(self.b**2 + radius**2)**0.5
    #         k = 1.0 if k > 1.0 else 0.0 if k < 0.0 else k
    #         angles.append(asin(k))
    #         angles.append(asin(-k))
    #     else:
    #         logger.error(f"Invalid given_var: {given_var}")
    #         logger.error(f"Valid given_var: {['x', 'y']}")
    #         raise Exception

    #     if use_deg:
    #         converted = []
    #         for angle in angles:
    #             converted.append(angle * 180 / pi)
    #         angles = converted
    #     return radius, angles, points

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
