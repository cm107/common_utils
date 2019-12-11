import numpy as np
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon

from logger import logger
from ..check_utils import check_type_from_list, check_value
from ..utils import get_class_string
from .common import Point, Interval
from .constants import number_types

class BBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        check_type_from_list(item_list=[xmin, ymin, xmax, ymax], valid_type_list=number_types)
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def __str__(self):
        return f"{get_class_string(self)}: (xmin, ymin, xmax, ymax)=({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return BBox(
            xmin=self.xmin,
            ymin=self.ymin,
            xmax=self.xmax,
            ymax=self.ymax
        )

    def to_int(self):
        return BBox(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax)
        )

    def to_float(self):
        return BBox(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax)
        )

    def to_list(self) -> list:
        return [self.xmin, self.ymin, self.xmax, self.ymax]

    def to_shapely(self) -> ShapelyPolygon:
        p0 = [self.xmin, self.ymin]
        p1 = [self.xmax, self.ymin]
        p2 = [self.xmax, self.ymax]
        p3 = [self.xmin, self.ymax]
        return ShapelyPolygon([p0, p1, p2, p3])

    def area(self) -> float:
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def shape(self) -> list:
        """
        return [height, width]
        """
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        return [height, width]

    def center(self) -> list:
        x_center = 0.5 * (self.xmin + self.xmax)
        y_center = 0.5 * (self.ymin + self.ymax)
        return [x_center, y_center]

    def aspect_ratio(self) -> float:
        """
        aspect ratio is height:width
        """
        height, width = self.shape()
        return height / width

    @classmethod
    def from_list(self, bbox: list):
        xmin, ymin, xmax, ymax = bbox
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    @classmethod
    def from_shapely(self, shapely_polygon: ShapelyPolygon):
        vals_tuple = shapely_polygon.exterior.coords.xy
        numpy_array = np.array(vals_tuple).T[:-1]
        if numpy_array.shape != (4, 2):
            logger.error(f"Expected shapely object of size (4, 2). Got {numpy_array.shape}")
            raise Exception
        xmin, ymin = numpy_array.min(axis=0)
        xmax, ymax = numpy_array.max(axis=0)
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def contains(self, obj) -> bool:
        return self.to_shapely().contains(obj.to_shapely())

    def within(self, obj) -> bool:
        return self.to_shapely().within(obj.to_shapely())

    def rescale(self, target_shape: list, fixed_point: Point):
        if fixed_point.x < self.xmin or fixed_point.x > self.xmax or \
            fixed_point.y < self.ymin or fixed_point.y > self.ymax:
            logger.error(f"fixed point {fixed_point} not inside bbox {self}")
            raise Exception
        left_dx, right_dx = fixed_point.x - self.xmin, self.xmax - fixed_point.x
        left_dy, right_dy = fixed_point.y - self.ymin, self.ymax - fixed_point.y
        bbox_h, bbox_w = self.shape()
        target_h, target_w = target_shape[:2]
        h_scale_factor, w_scale_factor = target_h / bbox_h, target_w / bbox_w
        new_left_dx, new_right_dx = left_dx * w_scale_factor, right_dx * w_scale_factor
        new_left_dy, new_right_dy = left_dy * h_scale_factor, right_dy * h_scale_factor
        new_xmin, new_xmax = fixed_point.x - new_left_dx, fixed_point.x + new_right_dx
        new_ymin, new_ymax = fixed_point.y - new_left_dy, fixed_point.y + new_right_dy
        new_bbox = BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
        return new_bbox

    def is_inside_of(self, bbox) -> bool:
        x_is_inside = True if bbox.xmin <= self.xmin and self.xmax <= bbox.xmax else False
        y_is_inside = True if bbox.ymin <= self.ymin and self.ymax <= bbox.ymax else False
        return x_is_inside and y_is_inside

    def encloses(self, bbox) -> bool:
        x_encloses = True if self.xmin <= bbox.xmin and bbox.xmax <= self.xmax else False
        y_encloses = True if self.ymin <= bbox.ymin and bbox.ymax <= self.ymax else False
        return x_encloses and y_encloses

    def overlaps_with(self, bbox) -> bool:
        x_overlaps = True if (bbox.xmin < self.xmin and self.xmin < bbox.xmax) \
            or (bbox.xmin < self.xmax and self.xmax < bbox.xmax) else False
        y_overlaps = True if (bbox.ymin < self.ymin and self.ymin < bbox.ymax) \
            or (bbox.ymin < self.ymax and self.ymax < bbox.ymax) else False
        return x_overlaps or y_overlaps

    def is_adjacent_with(self, bbox) -> bool:
        is_x_adjacent = True if bbox.xmax == self.xmin or self.xmax == bbox.xmin else False
        is_y_adjacent = True if bbox.ymax == self.ymin or self.ymax == bbox.ymin else False
        return is_x_adjacent and is_y_adjacent

    def center_is_inside_of(self, bbox) -> bool:
        cx, cy = self.center()
        x_is_inside = True if bbox.xmin <= cx and cx <= bbox.xmax else False
        y_is_inside = True if bbox.ymin <= cy and cy <= bbox.ymax else False
        return x_is_inside and y_is_inside

    def check_bbox_in_frame(self, frame_shape: list):
        frame_h, frame_w = frame_shape[:2]
        frame_box = BBox.from_list([0, 0, frame_w, frame_h])
        if not self.is_inside_of(frame_box):
            logger.error(f"bbox is not inside of frame_box")
            logger.error(f"bbox: {self.__str__()}")
            logger.error(f"frame_box: {frame_box}")
            raise Exception

    def check_bbox_aspect_ratio(self, target_aspect_ratio: float):
        if abs(self.aspect_ratio() - target_aspect_ratio) > 0.01:
            logger.error(f"Not creating the correct aspect ratio")
            logger.error(f"Target: {target_aspect_ratio}, actual: {self.aspect_ratio()}")
            raise Exception

    def pad(self, target_aspect_ratio: list, direction: str):
        """
        target_aspect_ratio corresponds to target_height:target_width
        """
        check_value(item=direction, valid_value_list=['x', 'y'])
        bbox_h, bbox_w = self.shape()
        bbox_cx, bbox_cy = self.center()

        if direction == 'x':
            target_bbox_h = bbox_h
            new_bbox_ymin, new_bbox_ymax = self.ymin, self.ymax
            target_bbox_w = bbox_h / target_aspect_ratio
            new_bbox_xmin, new_bbox_xmax = \
                bbox_cx - (0.5 * target_bbox_w), bbox_cx + (0.5 * target_bbox_w)
        elif direction == 'y':
            target_bbox_w = bbox_w
            new_bbox_xmin, new_bbox_xmax = self.xmin, self.xmax
            target_bbox_h = bbox_w * target_aspect_ratio
            new_bbox_ymin, new_bbox_ymax = \
                bbox_cy - (0.5 * target_bbox_h), bbox_cy + (0.5 * target_bbox_h)
        else:
            raise Exception

        return BBox.from_list([new_bbox_xmin, new_bbox_ymin, new_bbox_xmax, new_bbox_ymax])

    def is_adjacent_to_frame_bounds(self, frame_shape: list) -> (bool, bool, bool, bool):
        """
        returns: left_adjacent, top_adjacent, right_adjacent, bottom_adjacent
        """
        frame_h, frame_w = frame_shape[:2]
        left_adjacent = True if self.xmin == 0 else False
        top_adjacent = True if self.ymin == 0 else False
        right_adjacent = True if self.xmax == frame_w - 1 else False
        bottom_adjacent = True if self.ymax == frame_h - 1 else False
        return left_adjacent, top_adjacent, right_adjacent, bottom_adjacent

class ConstantAR_BBox(BBox):
    def __init__(self, xmin, ymin, xmax, ymax):
        super().__init__(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def from_BBox(self, bbox: BBox):
        return ConstantAR_BBox(xmin=bbox.xmin, ymin=bbox.ymin, xmax=bbox.xmax, ymax=bbox.ymax)

    def copy(self):
        return ConstantAR_BBox(
            xmin=self.xmin,
            ymin=self.ymin,
            xmax=self.xmax,
            ymax=self.ymax
        )

    def to_int(self):
        return ConstantAR_BBox(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax)
        )

    def to_float(self):
        return ConstantAR_BBox(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax)
        )

    @classmethod
    def from_list(self, bbox: list):
        xmin, ymin, xmax, ymax = bbox
        return ConstantAR_BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def rescale(self, target_shape: list, fixed_point: Point):
        return self.from_BBox(super().rescale(target_shape=target_shape, fixed_point=fixed_point))

    def pad(self, target_aspect_ratio: list, direction: str):
        return self.from_BBox(super().pad(target_aspect_ratio=target_aspect_ratio, direction=direction))

    def is_in_bounds(self, frame_shape: list) -> bool:
        frame_h, frame_w = frame_shape[:2]
        xmin_in_bounds = True if 0 <= self.xmin <= frame_w - 1 else False
        xmax_in_bounds = True if 0 <= self.xmax <= frame_w - 1 else False
        ymin_in_bounds = True if 0 <= self.ymin <= frame_h - 1 else False
        ymax_in_bounds = True if 0 <= self.ymax <= frame_h - 1 else False
        return xmin_in_bounds and xmax_in_bounds and ymin_in_bounds and ymax_in_bounds

    def adjust_to_frame_bounds(self, frame_shape: list):
        xmin, ymin, xmax, ymax = self.to_list()
        frame_h, frame_w = frame_shape[:2]
        xmin = 0 if xmin < 0 else frame_w - 1 if xmin >= frame_w else xmin
        ymin = 0 if ymin < 0 else frame_h - 1 if ymin >= frame_h else ymin
        xmax = 0 if xmax < 0 else frame_w - 1 if xmax >= frame_w else xmax
        ymax = 0 if ymax < 0 else frame_h - 1 if ymax >= frame_h else ymax
        result = ConstantAR_BBox.from_list([xmin, ymin, xmax, ymax])
        result.check_bbox_in_frame(frame_shape=frame_shape)
        return result

    def shift_bbox_in_bounds(self, frame_shape: list) -> (list, list, list):
        frame_h, frame_w = frame_shape[:2]
        x_interval = Interval.from_list([self.xmin, self.xmax])
        y_interval = Interval.from_list([self.ymin, self.ymax])
        x_bound = Interval.from_list([0, frame_w])
        y_bound = Interval.from_list([0, frame_h])
        x_is_in_bounds, [is_left_edge, is_right_edge], new_x_interval = \
            x_interval.shift_interval_in_bounds(bound=x_bound)
        y_is_in_bounds, [is_top_edge, is_bottom_edge], new_y_interval = \
            y_interval.shift_interval_in_bounds(bound=y_bound)
        [new_xmin, new_xmax] = new_x_interval.to_list() \
            if new_x_interval is not None else [None, None]
        [new_ymin, new_ymax] = new_y_interval.to_list() \
            if new_y_interval is not None else [None, None]
        bounds = [x_is_in_bounds, y_is_in_bounds]
        edge_orientation = [is_left_edge, is_right_edge, is_top_edge, is_bottom_edge]
        new_rect = [new_xmin, new_ymin, new_xmax, new_ymax]
        return bounds, edge_orientation, new_rect

    def rescale_bbox(self, target_aspect_ratio: list, pad_direction: str, mode: str='c'):
        mode = mode.lower()
        check_value(item=pad_direction.lower(), valid_value_list=['w', 'width', 'h', 'height'])
        check_value(item=mode, valid_value_list=['c', 'ct', 'cb', 'cr', 'cl', 'tr', 'tl', 'br', 'bl'])
        
        bbox_h, bbox_w = self.shape()
        if pad_direction.lower() in ['w', 'width']:
            target_w = bbox_w
            target_h = bbox_w * target_aspect_ratio
        elif pad_direction.lower() in ['h', 'height']:
            target_h = bbox_h
            target_w = bbox_h / target_aspect_ratio
        else:
            raise Exception

        target_shape = [target_h, target_w]

        [cx, cy] = self.center()
        top, bottom = self.ymin, self.ymax
        left, right = self.xmin, self.xmax

        if mode == 'c':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([cx, cy]))
        elif mode == 'ct':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([cx, top]))
        elif mode == 'cb':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([cx, bottom]))
        elif mode == 'cr':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([right, cy]))
        elif mode == 'cl':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([left, cy]))
        elif mode == 'tr':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([right, top]))
        elif mode == 'tl':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([left, top]))
        elif mode == 'br':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([right, bottom]))
        elif mode == 'bl':
            result = self.rescale(target_shape=target_shape, fixed_point=Point.from_list([left, bottom]))
        else:
            raise Exception
        result.check_bbox_aspect_ratio(target_aspect_ratio=target_aspect_ratio)
        return result

    def rescale_shift_bbox(self, frame_shape: list, target_aspect_ratio: float, pad_direction: str, mode: str='c') -> (list, list, list):
        result = self.rescale_bbox(target_aspect_ratio=target_aspect_ratio, pad_direction=pad_direction, mode=mode)
        bounds, edge_orientation, new_rect = result.shift_bbox_in_bounds(frame_shape=frame_shape)
        return bounds, edge_orientation, new_rect

    def rescale_shift_until_valid(self, frame_shape: list, target_aspect_ratio: float, max_retry_count: int=5):
        result = self
        mode = 'c'
        pad_direction = 'height'
        frame_h, frame_w = frame_shape[:2]
        retry_count = -1
        success = False

        backup = self.copy()

        while retry_count < max_retry_count:
            retry_count += 1
            bounds, edge_orientation, new_rect = result.rescale_shift_bbox(frame_shape=frame_shape, target_aspect_ratio=target_aspect_ratio, pad_direction=pad_direction, mode=mode)
            [x_is_in_bounds, y_is_in_bounds] = bounds
            [is_left_edge, is_right_edge, is_top_edge, is_bottom_edge] = edge_orientation
            [new_xmin, new_ymin, new_xmax, new_ymax] = new_rect
            if x_is_in_bounds and y_is_in_bounds:
                success = True
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
                break
            elif x_is_in_bounds and not y_is_in_bounds:
                new_ymin, new_ymax = 0, frame_h
                pad_direction = 'width'
                if is_left_edge and not is_right_edge:
                    mode = 'cl'
                elif is_right_edge and not is_left_edge:
                    mode = 'cr'
                else:
                    mode = 'c'
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
            elif not x_is_in_bounds and y_is_in_bounds:
                new_xmin, new_xmax = 0, frame_w
                pad_direction = 'height'
                if is_top_edge and not is_bottom_edge:
                    mode = 'ct'
                elif is_bottom_edge and not is_top_edge:
                    mode = 'cb'
                else:
                    mode = 'c'
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
            elif not x_is_in_bounds and not y_is_in_bounds:
                new_ymin, new_ymax = 0, frame_h
                new_xmin, new_xmax = 0, frame_w
                pad_direction = 'height'
                mode = 'c'
                result = ConstantAR_BBox.from_list([new_xmin, new_ymin, new_xmax, new_ymax])
            else:
                raise Exception

        if not success:
            logger.error(f"Couldn't obtain target aspect ratio within {max_retry_count} retries.")
            raise Exception

        result.check_bbox_aspect_ratio(target_aspect_ratio=target_aspect_ratio)
        return result

    def rescale_to_ar(self, target_aspect_ratio: float, hold_direction: str, hold_mode: str='center'):
        hold_direction = hold_direction.lower()
        check_value(item=hold_direction, valid_value_list=['x', 'y'])
        hold_mode = hold_mode.lower()
        check_value(item=hold_mode, valid_value_list=['center', 'min', 'max'])

        result = self.copy()
        if hold_direction == 'x':
            new_xmin, new_xmax = result.xmin, result.xmax
            new_width = new_xmax - new_xmin
            new_height = new_width * target_aspect_ratio
            if hold_mode == 'min':
                new_ymin = result.ymin
                new_ymax = new_ymin + new_height
            elif hold_mode == 'max':
                new_ymax = result.ymax
                new_ymin = new_ymax - new_height
            elif hold_mode == 'center':
                cy = 0.5 * (result.ymin + result.ymax)
                new_ymin = cy - (0.5 * new_height)
                new_ymax = cy + (0.5 * new_height)
            else:
                raise Exception
        elif hold_direction == 'y':
            new_ymin, new_ymax = result.ymin, result.ymax
            new_height = new_ymax - new_ymin
            new_width = new_height / target_aspect_ratio
            if hold_mode == 'min':
                new_xmin = result.xmin
                new_xmax = new_xmin + new_width
            elif hold_mode == 'max':
                new_xmax = result.xmax
                new_xmin = new_xmax - new_width
            elif hold_mode == 'center':
                cx = 0.5 * (result.xmin + result.xmax)
                new_xmin = cx - (0.5 * new_width)
                new_xmax = cx + (0.5 * new_width)
            else:
                raise Exception
        else:
            raise Exception
        return ConstantAR_BBox(xmin=new_xmin, ymin=new_ymin, xmax=new_xmax, ymax=new_ymax)

    def upscale_to_ar(self, target_aspect_ratio: float, hold_mode: str='center'):
        hold_mode = hold_mode.lower()
        check_value(item=hold_mode, valid_value_list=['center', 'min', 'max'])
        result = self.copy()

        aspect_ratio = result.aspect_ratio()
        if aspect_ratio > target_aspect_ratio: # too tall; expand width, hold y
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='y', hold_mode=hold_mode)
        else: # too wide; expand height, hold x
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='y', hold_mode=hold_mode)
        return result

    def downscale_to_ar(self, target_aspect_ratio: float, hold_mode: str='center'):
        hold_mode = hold_mode.lower()
        check_value(item=hold_mode, valid_value_list=['center', 'min', 'max'])
        result = self.copy()

        aspect_ratio = result.aspect_ratio()
        if aspect_ratio > target_aspect_ratio: # too tall; shrink height, hold x
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='x', hold_mode=hold_mode)
        else: # too wide; shrink width, hold y
            result = result.rescale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_direction='y', hold_mode=hold_mode)
        return result

    def try_upscale_to_ar(self, frame_shape: list, target_aspect_ratio: float, hold_mode: str):
        """
        Attempt upscale.
        Return None if bbox goes out of bounds.
        """
        result = self.copy()
        result = result.upscale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_mode=hold_mode)
        if result.is_in_bounds(frame_shape=frame_shape):
            return result
        else:
            return None

    def try_downscale_to_ar(self, frame_shape: list, target_aspect_ratio: float, hold_mode: str):
        """
        Attempt downscale.
        Return None if bbox goes out of bounds.
        """
        result = self.copy()
        result = result.downscale_to_ar(target_aspect_ratio=target_aspect_ratio, hold_mode=hold_mode)
        result = result.to_int()
        if result.is_in_bounds(frame_shape=frame_shape):
            return result
        else:
            return None

    def crop_scale(self, frame_shape: list, target_aspect_ratio: float):
        """
        1. First try upscale.
        2. Try downscale if upscale doesn't work.
        3. Preserve frame border adjacent sides of the bbox.
        """
        result = self.copy()
        result = result.adjust_to_frame_bounds(frame_shape=frame_shape)
        left_adj, top_adj, right_adj, bottom_adj = result.is_adjacent_to_frame_bounds(frame_shape)

        not_adj = not left_adj and not top_adj and not right_adj and not bottom_adj
        l_adj = left_adj and not top_adj and not right_adj and not bottom_adj
        t_adj = not left_adj and top_adj and not right_adj and not bottom_adj
        r_adj = not left_adj and not top_adj and right_adj and not bottom_adj
        b_adj = not left_adj and not top_adj and not right_adj and bottom_adj

        lt_adj = left_adj and top_adj
        rt_adj = right_adj and top_adj
        lb_adj = left_adj and bottom_adj
        rb_adj = right_adj and bottom_adj

        approach = 'upscale'

        if not_adj:
            hold_mode = 'center'
        elif l_adj or t_adj or lt_adj or rt_adj or lb_adj:
            hold_mode = 'min'
        elif rb_adj:
            hold_mode = 'max'
        else:
            hold_mode = 'center'

        while True:
            new_result = result.copy()
            if approach == 'upscale':
                new_result = new_result.try_upscale_to_ar(
                    frame_shape=frame_shape,
                    target_aspect_ratio=target_aspect_ratio,
                    hold_mode=hold_mode
                )
                if new_result is not None:
                    result = new_result
                    break
                else:
                    approach = 'downscale'
            elif approach == 'downscale':
                new_result = new_result.try_downscale_to_ar(
                    frame_shape=frame_shape,
                    target_aspect_ratio=target_aspect_ratio,
                    hold_mode=hold_mode
                )
                if new_result is not None:
                    result = new_result
                    break
                else:
                    logger.error(f"Couldn't resolve bbox.")
                    raise Exception
        return result

    def adjust_to_target_shape(
        self, frame_shape: list, target_shape: list, method: str='conservative_pad'
    ):
        check_value(item=method, valid_value_list=['pad', 'conservative_pad'])
        result = self
        if method == 'pad':
            target_h, target_w = target_shape[:2]
            target_aspect_ratio = target_h / target_w
            result = result.rescale_shift_until_valid(frame_shape=frame_shape, target_aspect_ratio=target_aspect_ratio, max_retry_count=5)
            result.check_bbox_in_frame(frame_shape=frame_shape)
        elif method == 'conservative_pad':
            target_h, target_w = target_shape[:2]
            target_aspect_ratio = target_h / target_w
            result = result.crop_scale(frame_shape=frame_shape, target_aspect_ratio=target_aspect_ratio)
        else:
            raise Exception
        return result