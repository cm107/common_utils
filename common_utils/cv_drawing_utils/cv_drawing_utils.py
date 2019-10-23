import cv2
import numpy as np
from ..common_types import Point, Size
from ..color_constants import Color
from ..check_utils import check_type_from_list
from ..image_utils import resize_img

class PointDrawer:
    def __init__(
        self, img: np.ndarray,
        radius: int=5, color: Color=Color.RED1
    ):
        self.img = img
        self.radius = radius
        self.color = color

    def set_radius(self, radius: int):
        self.radius = radius

    def set_color(self, color: Color):
        self.color = color

    def draw(
        self, point: Point,
        radius: int=None, color: Color=None
    ):
        if radius is not None:
            self.set_radius(radius)
        if color is not None:
            self.set_color(color)
        cv2.circle(
            img=self.img,
            center=point.to_tuple(),
            radius=self.radius,
            color=self.color,
            thickness=-1
        )

    def draw_point_list(
        self, point_list: list,
        radius: int=None, color: Color=None
    ):
        check_type_from_list(item_list=point_list, valid_type_list=[Point])
        if radius is not None:
            self.set_radius(radius)
        if color is not None:
            self.set_color(color)
        for point in point_list:
            self.draw(point.to_int())

    def get_image(self) -> np.ndarray:
        return self.img

def draw_mask_on_img(img: np.ndarray, mask: np.ndarray, color: list, scale: int, interpolation: str='area') -> np.ndarray:
    result = img.copy()
    working_mask = mask.copy()
    if img.shape[:2] != working_mask.shape[:2]:
        working_mask = resize_img(
            img=working_mask, size=Size.from_cv2_shape(img.shape), interpolation_method=interpolation
        )
    colored_mask = (
        (working_mask.reshape(-1).reshape(1, -1).T * color)
        .reshape(working_mask.shape[0], working_mask.shape[1], 3)
    ) / scale
    colored_mask = colored_mask.astype('uint8')
    cv2.addWeighted(src1=colored_mask, alpha=3, src2=result, beta=1, gamma=0, dst=result)
    return result