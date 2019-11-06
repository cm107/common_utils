from __future__ import annotations
import numpy as np
from logger import logger
from ..check_utils import check_type_from_list, check_value
from ..utils import get_class_string
from .common import Point, Interval

class BBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        check_type_from_list(item_list=[xmin, ymin, xmax, ymax], valid_type_list=[int, float, np.float64])
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def __str__(self):
        return f"{get_class_string(self)}: (xmin, ymin, xmax, ymax)=({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"

    def __repr__(self):
        return self.__str__()

    def to_int(self) -> BBox:
        return BBox(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax)
        )

    def to_float(self) -> BBox:
        return BBox(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax)
        )

    def to_list(self) -> list:
        return [self.xmin, self.ymin, self.xmax, self.ymax]

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
    def from_list(self, bbox: list) -> BBox:
        xmin, ymin, xmax, ymax = bbox
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def rescale(self, target_shape: list, fixed_point: Point) -> BBox:
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

    def is_inside_of(self, bbox: self) -> bool:
        x_is_inside = True if bbox.xmin <= self.xmin and self.xmax <= bbox.xmax else False
        y_is_inside = True if bbox.ymin <= self.ymin and self.ymax <= bbox.ymax else False
        return x_is_inside and y_is_inside

    def encloses(self, bbox: self) -> bool:
        x_encloses = True if self.xmin <= bbox.xmin and bbox.xmax <= self.xmax else False
        y_encloses = True if self.ymin <= bbox.ymin and bbox.ymax <= self.ymax else False
        return x_encloses and y_encloses

    def overlaps_with(self, bbox: self) -> bool:
        x_overlaps = True if (bbox.xmin < self.xmin and self.xmin < bbox.xmax) \
            or (bbox.xmin < self.xmax and self.xmax < bbox.xmax) else False
        y_overlaps = True if (bbox.ymin < self.ymin and self.ymin < bbox.ymax) \
            or (bbox.ymin < self.ymax and self.ymax < bbox.ymax) else False
        return x_overlaps or y_overlaps

    def is_adjacent_with(self, bbox: self) -> bool:
        is_x_adjacent = True if bbox.xmax == self.xmin or self.xmax == bbox.xmin else False
        is_y_adjacent = True if bbox.ymax == self.ymin or self.ymax == bbox.ymin else False
        return is_x_adjacent and is_y_adjacent

    def center_is_inside_of(self, bbox: self) -> bool:
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

    def pad(self, target_aspect_ratio: list, direction: str) -> BBox:
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

class ConstantAR_BBox(BBox):
    def __init__(self, xmin, ymin, xmax, ymax):
        super().__init__(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def from_BBox(self, bbox: BBox) -> ConstantAR_BBox:
        return ConstantAR_BBox(xmin=bbox.xmin, ymin=bbox.ymin, xmax=bbox.xmax, ymax=bbox.ymax)

    def to_int(self) -> ConstantAR_BBox:
        return ConstantAR_BBox(
            xmin=int(self.xmin),
            ymin=int(self.ymin),
            xmax=int(self.xmax),
            ymax=int(self.ymax)
        )

    def to_float(self) -> ConstantAR_BBox:
        return ConstantAR_BBox(
            xmin=float(self.xmin),
            ymin=float(self.ymin),
            xmax=float(self.xmax),
            ymax=float(self.ymax)
        )

    @classmethod
    def from_list(self, bbox: list) -> ConstantAR_BBox:
        xmin, ymin, xmax, ymax = bbox
        return ConstantAR_BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def rescale(self, target_shape: list, fixed_point: Point) -> ConstantAR_BBox:
        return self.from_BBox(super().rescale(target_shape=target_shape, fixed_point=fixed_point))

    def pad(self, target_aspect_ratio: list, direction: str) -> ConstantAR_BBox:
        return self.from_BBox(super().pad(target_aspect_ratio=target_aspect_ratio, direction=direction))

    def adjust_to_frame_bounds(self, frame_shape: list) -> ConstantAR_BBox:
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

    def rescale_bbox(self, target_aspect_ratio: list, pad_direction: str, mode: str='c') -> ConstantAR_BBox:
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

    def rescale_shift_until_valid(self, frame_shape: list, target_aspect_ratio: list, max_retry_count: int=5) -> ConstantAR_BBox:
        result = self
        mode = 'c'
        pad_direction = 'height'
        frame_h, frame_w = frame_shape[:2]
        retry_count = -1
        success = False

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

    def adjust_to_target_shape(
        self, frame_shape: list, target_shape: list, method: str='pad'
    ) -> ConstantAR_BBox:
        check_value(item=method, valid_value_list=['pad'])
        result = self
        if method == 'pad':
            target_h, target_w = target_shape[:2]
            target_aspect_ratio = target_h / target_w
            result = result.rescale_shift_until_valid(frame_shape=frame_shape, target_aspect_ratio=target_aspect_ratio, max_retry_count=5)
            result.check_bbox_in_frame(frame_shape=frame_shape)
        else:
            raise Exception
        return result