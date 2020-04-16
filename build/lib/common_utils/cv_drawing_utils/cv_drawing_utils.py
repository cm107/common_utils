from typing import List
import cv2
import numpy as np

from logger import logger

from ..common_types import Point, Size
from ..common_types.bbox import BBox
from ..common_types.segmentation import Segmentation
from ..color_constants import Color
from ..check_utils import check_type_from_list, check_type
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
def draw_bbox_text(img: np.ndarray, bbox: BBox, text: str, color: list=[0, 255, 255], font_face: int=cv2.FONT_HERSHEY_COMPLEX, thickness: int=2) -> np.ndarray:
    result = img.copy()
    bbox_h, bbox_w = bbox.shape()
    target_textbox_w = bbox_w
    font_scale = 1 * (target_textbox_w / 93)

    [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    retry_count = 0
    while abs(textbox_w - target_textbox_w) / target_textbox_w > 0.1 and retry_count < 3:
        retry_count += 1
        font_scale = font_scale * (target_textbox_w / textbox_w)
        [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    textbox_org_x = int(0.5 * (target_textbox_w - textbox_w) + bbox.xmin)
    textbox_org_y = int(bbox.ymin - 0.3 * textbox_h)
    textbox_org = (textbox_org_x, textbox_org_y)
    cv2.putText(img=result, text=text, org=textbox_org, fontFace=font_face, fontScale=font_scale, color=color, thickness=thickness, bottomLeftOrigin=False)
    return result

def draw_text_inside_bbox(img: np.ndarray, bbox: BBox, text: str, color: list=[0, 255, 255], font_face: int=cv2.FONT_HERSHEY_COMPLEX, thickness: int=2) -> np.ndarray:
    result = img.copy()
    bbox_h, bbox_w = bbox.shape()
    target_textbox_w = bbox_w
    font_scale = 1 * (target_textbox_w / 93)

    [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    retry_count = 0
    while abs(textbox_w - target_textbox_w) / target_textbox_w > 0.1 and retry_count < 3:
        retry_count += 1
        font_scale = font_scale * (target_textbox_w / textbox_w)
        [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    height_adjustment_count = 0
    while textbox_h >= bbox_h and height_adjustment_count < 3:
        height_adjustment_count += 1
        font_scale = font_scale * (bbox_h / textbox_h)
        [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)

    textbox_org_x = int(0.5 * (target_textbox_w - textbox_w) + bbox.xmin)
    textbox_org_y = int(bbox.ymin + 0.5 * (bbox_h + textbox_h))
    textbox_org = (textbox_org_x, textbox_org_y)
    cv2.putText(img=result, text=text, org=textbox_org, fontFace=font_face, fontScale=font_scale, color=color, thickness=thickness, bottomLeftOrigin=False)
    return result

def draw_text_at_point(
    img: np.ndarray, text: str, x: int, y: int, target_height: int,
    leeway: float=0.4, color: list=[0, 255, 255], font_face: int=cv2.FONT_HERSHEY_COMPLEX, thickness: int=2
) -> np.ndarray:
    result = img.copy()
    target_text_h = target_height * (1 - leeway)
    font_scale = 1 * (target_text_h / 10)
    [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    retry_count = 0
    while abs(textbox_h - target_text_h) / target_text_h > 0.1 and textbox_h >= target_text_h and retry_count < 3:
        retry_count += 1
        font_scale = font_scale * (target_text_h / textbox_h)
        [textbox_w, textbox_h], _ = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
    textbox_org_x = int(x)
    textbox_org_y = int(y + textbox_h + 0.5 * leeway * target_height)
    textbox_org = (textbox_org_x, textbox_org_y)
    cv2.putText(img=result, text=text, org=textbox_org, fontFace=font_face, fontScale=font_scale, color=color, thickness=thickness, bottomLeftOrigin=False)
    return result

def draw_text_rows_at_point(
    img: np.ndarray, row_text_list: List[str], x: int, y: int, combined_row_height: int,
    leeway: float=0.4, color: list=[0, 255, 255], font_face: int=cv2.FONT_HERSHEY_COMPLEX, thickness: int=2
) -> np.ndarray:
    result = img.copy()
    n_rows = len(row_text_list)
    row_height = int(combined_row_height / n_rows)
    y_coord_list = [y + row_height * i for i in range(n_rows)]
    for row_text, y_coord in zip(row_text_list, y_coord_list):
        result = draw_text_at_point(
            img=result, text=row_text, x=x, y=y_coord, target_height=row_height,
            leeway=leeway, color=color, font_face=font_face, thickness=thickness
        )
    return result

def draw_bbox(img: np.ndarray, bbox: BBox, color: list=[0, 255, 255], thickness: int=2, text: str=None, label_thickness: int=None, label_only: bool=False) -> np.ndarray:
    result = img.copy()
    xmin, ymin, xmax, ymax = bbox.to_int().to_list()
    if not (text is not None and label_only):
        cv2.rectangle(img=result, pt1=(xmin, ymin), pt2=(xmax, ymax), color=color, thickness=thickness)
    if text is not None:
        text_thickness = label_thickness if label_thickness is not None else thickness
        result = draw_bbox_text(img=result, bbox=bbox, text=text, color=color, thickness=text_thickness)
    return result

def draw_keypoints_labels(
    img: np.ndarray, keypoints: list, keypoint_labels: list, color: list=[0, 0, 255], font_face: int=cv2.FONT_HERSHEY_COMPLEX, thickness: int=1,
    ignore_kpt_idx: list=[]
):
    result = img.copy()

    # Define BBox enclosing keypoints
    np_kpts = np.array(keypoints)
    if len(np_kpts) > 0:
        kpts_xmin, kpts_ymin = np.min(np_kpts, axis=0)
        kpts_xmax, kpts_ymax = np.max(np_kpts, axis=0)
        kpts_bbox = BBox(xmin=kpts_xmin, ymin=kpts_ymin, xmax=kpts_xmax, ymax=kpts_ymax)
        bbox_h, bbox_w = kpts_bbox.shape()
        
        # Define target_textbox_w and initial font_scale guess.
        target_textbox_w = 0.1 * bbox_w # Needs adjustment
        font_scale = 1 * (target_textbox_w / 93)

        # Find max_size_label_idx
        textbox_w, textbox_h = None, None
        max_size_label_idx = None
        for i, keypoint_label in enumerate(keypoint_labels):
            [label_w, label_h], _ = cv2.getTextSize(text=keypoint_label, fontFace=font_face, fontScale=font_scale, thickness=thickness)
            if textbox_w is None or label_w > textbox_w:
                textbox_w, textbox_h = label_w, label_h
                max_size_label_idx = i

        # Adjust to target_textbox_w
        retry_count = 0
        while abs(textbox_w - target_textbox_w) / target_textbox_w > 0.1 and retry_count < 3:
            retry_count += 1
            font_scale = font_scale * (target_textbox_w / textbox_w)
            [textbox_w, textbox_h], _ = cv2.getTextSize(text=keypoint_labels[max_size_label_idx], fontFace=font_face, fontScale=font_scale, thickness=thickness)
        
        # Draw Label
        for i, [[x, y], keypoint_label] in enumerate(zip(keypoints, keypoint_labels)):
            if i not in ignore_kpt_idx:
                textbox_org_x = int(x - 0.5 * textbox_w)
                textbox_org_y = int(y - 0.5 * textbox_h)
                textbox_org = (textbox_org_x, textbox_org_y)
                cv2.putText(
                    img=result, text=keypoint_label, org=textbox_org, fontFace=font_face, fontScale=font_scale, color=color,
                    thickness=thickness, bottomLeftOrigin=False
                )
    return result

def draw_keypoints(
    img: np.ndarray, keypoints: list,
    radius: int=4, color: list=[0, 0, 255],
    keypoint_labels: list=None, show_keypoints_labels: bool=False, label_thickness: int=1, label_only: bool=False,
    ignore_kpt_idx: list=[]
) -> np.ndarray:
    result = img.copy()
    if not (keypoint_labels is not None and label_only):
        for i, [x, y] in enumerate(keypoints):
            if i not in ignore_kpt_idx:
                cv2.circle(
                    result,
                    (int(x), int(y)),
                    radius,
                    color,
                    -1,
                )
    if show_keypoints_labels or label_only:
        if keypoint_labels is not None:
            result = draw_keypoints_labels(
                img=result, keypoints=keypoints, keypoint_labels=keypoint_labels, color=color, thickness=label_thickness,
                ignore_kpt_idx=ignore_kpt_idx
            )
        else:
            logger.error(f"Need to provide keypoint_labels in order to show labels.")
            raise Exception
    return result

def draw_skeleton(
    img: np.ndarray, keypoints: np.ndarray, keypoint_skeleton: list, index_offset: int=0, thickness: int=5, color: list=[255, 0, 0],
    color_list: list=None, ignore_kpt_idx: list=[]
) -> np.ndarray:
    check_type(keypoints, valid_type_list=[list, tuple, np.ndarray])
    if type(keypoints) is np.ndarray:
        kpts = keypoints.tolist()
    elif type(keypoints) is list or type(keypoints) is tuple:
        kpts = keypoints
    else:
        raise Exception
    result = img.copy()
    if len(kpts) > 0:
        color_list = [color] * len(keypoint_skeleton) if color_list is None else color_list
        if len(color_list) != len(keypoint_skeleton):
            logger.error(f"Length Mismatch: len(color_list) == {len(color_list)} != {len(keypoint_skeleton)} == len(keypoint_skeleton)")
            raise Exception
        flat_skeleton = np.array(keypoint_skeleton).reshape(-1)+index_offset
        if np.any(flat_skeleton < 0):
            logger.error(f'Found a negative index. Currently using index_offset={index_offset}')
            min_idx = np.min(flat_skeleton)
            logger.error(f'Minimum index found: {min_idx}')
            logger.error(f'Please use index_offset={-min_idx+index_offset}')
            raise IndexError
        if np.any(flat_skeleton >= len(keypoints)):
            logger.error(f'Found index that exceeds size of keypoint array ({len(keypoints)}). Currently using index_offset={index_offset}')
            max_idx = np.max(flat_skeleton)
            logger.error(f'Maximum index found: {max_idx}')
            logger.error(f'Please use index_offset={-(max_idx-(len(keypoints)-1))+index_offset}')
            raise IndexError
        for [joint_start_index, joint_end_index], joint_color in zip(keypoint_skeleton, color_list):
            if joint_start_index+index_offset not in ignore_kpt_idx and joint_end_index+index_offset not in ignore_kpt_idx:
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
        result = cv2.drawContours(image=result, contours=segmentation.to_contour(), contourIdx=-1, color=color, thickness=-1)
    else:
        mask = np.zeros(img.shape[:2], np.uint8)
        mask = cv2.drawContours(image=mask, contours=segmentation.to_contour(), contourIdx=-1, color=(255, 255, 255), thickness=-1)
        result = draw_mask_on_img(img=result, mask=mask, color=color, scale=255)
    return result