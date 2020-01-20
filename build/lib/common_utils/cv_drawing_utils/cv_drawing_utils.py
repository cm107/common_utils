import cv2
import numpy as np

from logger import logger

from ..common_types import Point, Size
from ..common_types.bbox import BBox
from ..common_types.segmentation import Segmentation
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

# Basic
def draw_bbox_text(img: np.ndarray, bbox: BBox, text: str, color: list=[0, 255, 255], font_face: int=cv2.FONT_HERSHEY_COMPLEX, thickness: int=2):
    result = img.copy()
    bbox_h, bbox_w = bbox.shape()
    font_scale = 1 * (bbox_w / 93) # Needs adjustment
    [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    retry_count = 0
    while abs(textbox_w - bbox_w) / bbox_w > 0.1 and retry_count < 3:
        retry_count += 1
        font_scale = font_scale * (bbox_w / textbox_w)
        [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    textbox_org_x = int(0.5 * (bbox_w - textbox_w) + bbox.xmin)
    textbox_org_y = int(bbox.ymin - 0.3 * textbox_h)
    textbox_org = (textbox_org_x, textbox_org_y)
    cv2.putText(img=result, text=text, org=textbox_org, fontFace=font_face, fontScale=font_scale, color=color, thickness=thickness, bottomLeftOrigin=False)
    return result

def draw_bbox(img: np.ndarray, bbox: BBox, color: list=[0, 255, 255], thickness: int=2, text: str=None) -> np.ndarray:
    result = img.copy()
    xmin, ymin, xmax, ymax = bbox.to_int().to_list()
    cv2.rectangle(img=result, pt1=(xmin, ymin), pt2=(xmax, ymax), color=color, thickness=thickness)
    if text is not None:
        result = draw_bbox_text(img=result, bbox=bbox, text=text, color=color, thickness=thickness)
    return result

def draw_keypoints(img: np.ndarray, keypoints: list, radius: int=10, color: list=[0, 0, 255]) -> np.ndarray:
    result = img.copy()
    for x, y in keypoints:
        cv2.circle(
            result,
            (int(x), int(y)),
            radius,
            color,
            -1,
        )
    return result

def draw_skeleton(
    img: np.ndarray, keypoints: np.ndarray, keypoint_skeleton: list, index_offset: int=0, thickness: int=5, color: list=[255, 0, 0],
    color_list: list=None
) -> np.ndarray:
    result = img.copy()
    kpts = keypoints.tolist()
    color_list = [color] * len(keypoint_skeleton) if color_list is None else color_list
    if len(color_list) != len(keypoint_skeleton):
        logger.error(f"Length Mismatch: len(color_list) == {len(color_list)} != {len(keypoint_skeleton)} == len(keypoint_skeleton)")
        raise Exception
    for [joint_start_index, joint_end_index], joint_color in zip(keypoint_skeleton, color_list):
        line_start_x, line_start_y = kpts[joint_start_index+index_offset]
        line_end_x, line_end_y = kpts[joint_end_index+index_offset]
        cv2.line(
            img=result,
            pt1=(int(line_start_x), int(line_start_y)),
            pt2=(int(line_end_x), int(line_end_y)),
            color=joint_color,
            thickness=thickness
        )
    return result

def draw_bool_mask(
    img: np.ndarray, mask: np.ndarray, color: list=[255, 255, 0], transparent: bool=False
):
    result = img.copy()
    if not transparent:
        result[mask] = color
    else:
        working_mask = np.zeros(shape=result.shape[:2], dtype=np.uint8)
        working_mask[mask] = 255
        result = draw_mask_on_img(img=result, mask=working_mask, color=color, scale=255)
    return result

def draw_segmentation(
    img: np.ndarray, segmentation: Segmentation, color: list=[255, 255, 0], transparent: bool=False
):
    result = img.copy()
    if not transparent:
        result = cv2.drawContours(image=result, contours=segmentation.to_contour(), contourIdx=0, color=color, thickness=-1)
    else:
        mask = np.zeros(img.shape[:2], np.uint8)
        mask = cv2.drawContours(image=mask, contours=segmentation.to_contour(), contourIdx=0, color=(255, 255, 255), thickness=-1)
        result = draw_mask_on_img(img=result, mask=mask, color=color, scale=255)
    return result