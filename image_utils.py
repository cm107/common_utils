import cv2
import numpy as np
from .common_types import Size
from ..logger.logger_handler import logger

def get_scaled_dims(width: int, height: int, scale_factor) -> (int, int):
    return int(width * scale_factor), int(height * scale_factor)

def scale_img(frame: np.ndarray, scale_factor) -> np.ndarray:
    height, width = frame.shape[:2]
    downsized_width, downsized_height = get_scaled_dims(width, height, scale_factor)

    if scale_factor == 1.0:    
        return frame
    elif scale_factor > 0.0 and scale_factor < 1.0:
        return cv2.resize(
            frame,
            (downsized_width, downsized_height),
            interpolation=cv2.INTER_AREA)
    elif scale_factor > 1.0:
        return cv2.resize(
            frame,
            (downsized_width, downsized_height),
            interpolation=cv2.INTER_LINEAR)
    else:
        raise Exception(f"Invalid scale_factor={scale_factor}. Expected scale_factor > 0.")

def get_grayscale(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def get_size(img: np.ndarray) -> Size:
    height, width = img.shape[:2]
    return Size(width=width, height=height)

def resize_img0(img: np.ndarray, size: Size) -> np.ndarray:
    img_size = get_size(img)
    if size.area >= img_size.area:
        return cv2.resize(
            src=img, dsize=(size.width, size.height), interpolation=cv2.INTER_LINEAR
        )
    else:
        return cv2.resize(
            src=img, dsize=(size.width, size.height), interpolation=cv2.INTER_AREA
        )

def resize_img(img: np.ndarray, size: Size, interpolation_method: str='area') -> np.ndarray:
    possible_methods = ['area', 'linear']
    if interpolation_method.lower() == 'area':
        interpolation = cv2.INTER_AREA
    elif interpolation_method.lower() == 'linear':
        interpolation = cv2.INTER_LINEAR
    else:
        logger.error(f"Invalid interpolation_method: {interpolation_method}")
        logger.error(f"Possible choices for interpolation_method:")
        for possible_method in possible_methods:
            logger.error(f"\t{possible_method}")
        raise Exception
    return cv2.resize(
        src=img, dsize=(size.width, size.height), interpolation=interpolation
    )

def show_cv2_image(img: np.ndarray, title: str='Test', window_size: Size=None):
    if img.dtype is np.dtype('int64'):
        image = img.astype('uint8')
    else:
        image = img.copy()
    cv2.namedWindow(winname=title, flags=cv2.WINDOW_NORMAL)
    if window_size is not None:
        cv2.resizeWindow(winname=title, width=window_size.width, height=window_size.height)
    cv2.imshow(title, image)
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()