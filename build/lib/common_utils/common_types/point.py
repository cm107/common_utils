import numpy as np
from shapely.geometry import Point as ShapelyPoint

from logger import logger

from .constants import number_types
from ..check_utils import check_type, check_type_from_list
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
    
    def to_int(self):
        return Point(coords=[int(val) for val in self.coords])

    def to_float(self):
        return Point(coords=[float(val) for val in self.coords])

    def to_list(self) -> list:
        return self.coords

    def to_shapely(self) -> ShapelyPoint:
        return ShapelyPoint(self.to_list())

    @classmethod
    def from_list(self, coords: list):
        return Point(coords=coords)

    @classmethod
    def from_shapely(self, shapely_point: ShapelyPoint):
        return Point(coords=[list(val)[0] for val in shapely_point.coords.xy])

    def within(self, obj) -> bool:
        return self.to_shapely().within(obj.to_shapely())