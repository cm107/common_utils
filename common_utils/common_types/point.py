from __future__ import annotations
import numpy as np
from shapely.geometry import Point as ShapelyPoint

from logger import logger

from .constants import number_types
from ..check_utils import check_type, check_type_from_list, check_list_length
from ..utils import get_class_string

class Point:
    def __init__(self, coords: list):
        check_type(item=coords, valid_type_list=[list])
        check_type_from_list(item_list=coords, valid_type_list=number_types)
        self.coords = coords
        self.dimensionality = len(coords)

    def __str__(self):
        return f"{get_class_string(self)}: {self.coords}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def buffer(self, point: Point) -> Point:
        return point

    def copy(self) -> Point:
        return Point(coords=self.coords)

    def to_int(self) -> Point:
        return Point(coords=[int(val) for val in self.coords])

    def to_float(self) -> Point:
        return Point(coords=[float(val) for val in self.coords])

    def to_list(self) -> list:
        return self.coords

    def to_shapely(self) -> ShapelyPoint:
        return ShapelyPoint(self.to_list())

    @classmethod
    def from_list(self, coords: list) -> Point:
        return Point(coords=coords)

    @classmethod
    def from_shapely(self, shapely_point: ShapelyPoint) -> Point:
        return Point(coords=[list(val)[0] for val in shapely_point.coords.xy])

    def within(self, obj) -> bool:
        return self.to_shapely().within(obj.to_shapely())

class Point2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point2D({self.x},{self.y})"

    def __repr__(self):
        return self.__str__()

    def to_list(self) -> list:
        return [self.x, self.y]

    @classmethod
    def from_list(cls, coords: list) -> Point3D:
        check_list_length(coords, correct_length=2)
        return Point2D(x=coords[0], y=coords[1])

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point3D({self.x},{self.y},{self.z})"

    def __repr__(self):
        return self.__str__()

    def to_list(self) -> list:
        return [self.x, self.y, self.z]

    @classmethod
    def from_list(cls, coords: list) -> Point3D:
        check_list_length(coords, correct_length=3)
        return Point3D(x=coords[0], y=coords[1], z=coords[2])