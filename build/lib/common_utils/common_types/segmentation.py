from __future__ import annotations
import numpy as np
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from shapely.ops import cascaded_union

from logger import logger

from .constants import number_types
from ..check_utils import check_type, check_type_from_list
from ..utils import get_class_string

from .point import Point
from .bbox import BBox

class Polygon:
    def __init__(self, points: list, dimensionality: int=2):
        check_type(item=points, valid_type_list=[list])
        check_type_from_list(item_list=points, valid_type_list=number_types)
        check_type(item=dimensionality, valid_type_list=[int])
        if len(points) % dimensionality != 0:
            logger.error(f"len(points) is not divisible by dimensionality={dimensionality}")
            raise Exception

        self.points = points
        self.dimensionality = dimensionality

    def __str__(self):
        return f"{get_class_string(self)}: {self.points}"

    def __repr__(self):
        return self.__str__()
    
    def to_int(self) -> Polygon:
        return Polygon(points=[int(val) for val in self.points], dimensionality=self.dimensionality)

    def to_float(self) -> Polygon:
        return Polygon(points=[float(val) for val in self.points], dimensionality=self.dimensionality)

    def to_list(self, demarcation: bool=False) -> list:
        if demarcation:
            return np.array(self.points).reshape(-1, self.dimensionality).tolist()
        else:
            return self.points

    def to_point_list(self) -> list:
        return [Point(coords=coords) for coords in self.to_list(demarcation=True)]

    def to_shapely(self) -> ShapelyPolygon:
        return ShapelyPolygon(self.to_list(demarcation=True))

    def to_bbox(self) -> BBox:
        points = np.array(self.to_list(demarcation=True))
        xmin, ymin = points.min(axis=0)
        xmax, ymax = points.max(axis=0)
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def area(self) -> float:
        return self.to_shapely().area
    
    def centroid(self) -> Point:
        return Point.from_shapely(self.to_shapely().centroid)

    def contains_point(self, point: Point) -> bool:
        return self.to_shapely().contains(point.to_shapely())

    def contains_polygon(self, polygon: Polygon) -> bool:
        return self.to_shapely().contains(polygon.to_shapely())

    def contains_bbox(self, bbox: BBox) -> bool:
        return self.to_shapely().contains(bbox.to_shapely())

    def contains(self, obj) -> bool:
        check_type(item=obj, valid_type_list=[Point, Polygon, BBox])
        return self.to_shapely().contains(obj.to_shapely())

    def within_polygon(self, polygon: Polygon) -> bool:
        return self.to_shapely().within(polygon.to_shapely())

    def within_bbox(self, bbox: BBox) -> bool:
        return self.to_shapely().within(bbox.to_shapely())

    def within(self, obj) -> bool:
        check_type(item=obj, valid_type_list=[Polygon, BBox])
        return self.to_shapely().within(obj.to_shapely())

    def intersects_polygon(self, polygon: Polygon) -> bool:
        return self.to_shapely().intersects(polygon)

    def size(self) -> tuple:
        return np.array(self.points).reshape(-1, self.dimensionality).shape

    @classmethod
    def from_list(self, points: list, dimensionality: int=2, demarcation: bool=False) -> Polygon:
        if demarcation:
            flattened_list = np.array(points).reshape(-1).tolist()
            return Polygon(points=flattened_list, dimensionality=dimensionality)
        else:
            return Polygon(points=points, dimensionality=dimensionality)

    @classmethod
    def from_point_list(self, point_list: list, dimensionality: int=2) -> Polygon:
        check_type_from_list(item_list=point_list, valid_type_list=[Point])
        result = []
        for i, point in enumerate(point_list):
            numpy_array = np.array(point.to_list())
            if numpy_array.shape != (dimensionality,):
                logger.error(f"Found point at index {i} of point_list with a shape of {numpy_array.shape} != {(dimensionality,)}")
                raise Exception
            result.extend(point.to_list())
        return Polygon(points=result, dimensionality=dimensionality)

    @classmethod
    def from_shapely(self, shapely_polygon: ShapelyPolygon) -> Polygon:
        vals_tuple = shapely_polygon.exterior.coords.xy
        numpy_array = np.array(vals_tuple).T[:-1]
        flattened_list = numpy_array.reshape(-1).tolist()
        dimensionality = numpy_array.shape[1]
        return Polygon(points=flattened_list, dimensionality=dimensionality)

    @classmethod
    def from_contour(self, contour: np.ndarray) -> Polygon:
        cont = contour.reshape(contour.shape[0], contour.shape[2]).tolist()
        return self.from_list(points=cont, dimensionality=2, demarcation=True)

    @classmethod
    def from_polygon_list_to_merge(self, polygon_list: list) -> Polygon:
        from shapely.geometry import MultiPolygon as ShapelyMultiPolygon
        import matplotlib.pyplot as plt
        import geopandas as gpd

        valid_polygon_list = []
        for polygon in polygon_list:
            if polygon.size()[0] > 2: # Filter out polygons with less than 3 vertices.
                valid_polygon_list.append(polygon)
        # logger.red(valid_polygon_list)
        merged_polygon = None
        for i, valid_polygon in enumerate(valid_polygon_list):
            if merged_polygon is None:
                merged_polygon = valid_polygon.to_shapely()
                logger.yellow(f"{i+1}/{len(valid_polygon_list)}: type(merged_polygon): {type(merged_polygon)}")
            else:
                if merged_polygon.intersects(valid_polygon.to_shapely()):
                    logger.green(f"intersects!")
                else:
                    logger.red(f"Not intersects!")
                if type(merged_polygon) is ShapelyPolygon:
                    logger.cyan(f"Flag0")
                    polygons = gpd.GeoSeries(merged_polygon)
                    new_polygon = gpd.GeoSeries(valid_polygon.to_shapely())
                    polygons.plot()
                    new_polygon.plot()
                    plt.show()
                    if not merged_polygon.is_valid:
                        logger.error(f"merged_polygon is not valid")
                        raise Exception
                    if not valid_polygon.to_shapely().is_valid:
                        logger.error(f"New polygon is not valid")
                        raise Exception
                    if merged_polygon.intersects(valid_polygon.to_shapely()):
                        merged_polygon = merged_polygon.union(valid_polygon.to_shapely())
                    else:
                        merged_polygon = cascaded_union([merged_polygon, valid_polygon.to_shapely()])
                    if type(merged_polygon) is ShapelyMultiPolygon:
                        logger.cyan(f"Hull")
                        merged_polygon = merged_polygon.convex_hull
                        if type(merged_polygon) is ShapelyPolygon:
                            logger.green(f"Fixed!")
                        elif type(merged_polygon) is ShapelyMultiPolygon:
                            logger.error(f"Not Fixed!")
                            raise Exception
                        else:
                            logger.error(f"Unknown type: {type(merged_polygon)}")
                            raise Exception
                elif type(merged_polygon) is ShapelyMultiPolygon:
                    logger.error(f"Polygon turned into MultiPolygon in shapely!")
                    raise Exception
                else:
                    logger.error(f"type(merged_polygon): {type(merged_polygon)}")
                    raise Exception

                logger.yellow(f"{i+1}/{len(valid_polygon_list)}: type(merged_polygon): {type(merged_polygon)}")
                # logger.yellow(f"{i+1}/{len(valid_polygon_list)}: type(merged_polygon.exterior): {type(merged_polygon.exterior)}")
            logger.blue(f"{i+1}/{len(valid_polygon_list)}: valid_polygon.size(): {valid_polygon.size()}")

        import sys
        sys.exit()
        union = cascaded_union([valid_polygon.to_shapely() for valid_polygon in valid_polygon_list])
        return self.from_shapely(union)

class Segmentation:
    def __init__(self, polygon_list: list):
        check_type(item=polygon_list, valid_type_list=[list])
        check_type_from_list(item_list=polygon_list, valid_type_list=[Polygon])
        for i, polygon in enumerate(polygon_list):
            if polygon.dimensionality != 2:
                logger.error(f"Found polygon of dimensionality {polygon.dimensionality} at index {i}")
                logger.error(f"All polygons must be of dimensionality 2.")
                raise Exception
        self.polygon_list = polygon_list

    def __str__(self):
        return f"{get_class_string(self)}: {self.polygon_list}"

    def __repr__(self):
        return self.__str__()

    def to_int(self) -> Polygon:
        return Segmentation([polygon.to_int() for polygon in self.polygon_list])

    def to_float(self) -> Polygon:
        return Segmentation([polygon.to_float() for polygon in self.polygon_list])

    def to_list(self, demarcation: bool=False) -> list:
        return [polygon.to_list(demarcation=demarcation) for polygon in self.polygon_list]

    def to_point_list(self) -> list:
        return [polygon.to_point_list() for polygon in self.polygon_list]

    def to_shapely(self) -> list:
        return [polygon.to_shapely() for polygon in self.polygon_list]

    def to_bbox(self) -> list:
        return [polygon.to_bbox() for polygon in self.polygon_list]

    def area(self) -> list:
        return [polygon.area() for polygon in self.polygon_list]
    
    def centroid(self) -> list:
        return [polygon.centroid() for polygon in self.polygon_list]

    def contains_point(self, point: Point) -> list:
        return [polygon.contains_point() for polygon in self.polygon_list]

    def contains_polygon(self, polygon: Polygon) -> list:
        return [polygon.contains_polygon() for polygon in self.polygon_list]

    def contains_bbox(self, bbox: BBox) -> list:
        return [polygon.contains_bbox() for polygon in self.polygon_list]

    def contains(self, obj) -> list:
        check_type(item=obj, valid_type_list=[Point, Polygon, BBox])
        return [polygon.contains() for polygon in self.polygon_list]

    def within_polygon(self, polygon: Polygon) -> list:
        return [polygon.within_polygon() for polygon in self.polygon_list]

    def within_bbox(self, bbox: BBox) -> list:
        return [polygon.within_bbox() for polygon in self.polygon_list]

    def within(self, obj) -> list:
        check_type(item=obj, valid_type_list=[Polygon, BBox])
        return [polygon.within() for polygon in self.polygon_list]

    def merge(self) -> Segmentation:
        return Segmentation(
            polygon_list=[Polygon.from_polygon_list_to_merge(
                polygon_list=self.polygon_list
            )]
        )

    @classmethod
    def from_list(self, points_list: list, demarcation: bool=False) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_list(
                    points=points, dimensionality=2, demarcation=demarcation
                ) for points in points_list
            ]
        )

    @classmethod
    def from_point_list(self, point_list_list: list) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_point_list(
                    point_list=point_list, dimensionality=2
                ) for point_list in point_list_list
            ]
        )

    @classmethod
    def from_shapely(self, shapely_polygon_list: list) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_shapely(
                    shapely_polygon=shapely_polygon
                ) for shapely_polygon in shapely_polygon_list
            ]
        )

    @classmethod
    def from_contour(self, contour_list: list) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_contour(
                    contour=contour
                ) for contour in contour_list
            ]
        )