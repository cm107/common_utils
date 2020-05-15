from logger import logger
from common_utils.common_types.segmentation import Segmentation, Polygon
import numpy as np

contours = [
    np.array(
        [
            [[0, 0]],
            [[1, 0]],
            [[1, 2]],
            [[0, 1]]
        ]
    ),
    np.array(
        [
            [[0, 0]],
            [[1, 0]],
            [[1, 2]],
            [[0, 1]]
        ]
    ),
    np.array(
        [
            [[1, 0]],
            [[2, 0]],
            [[2, 2]],
            [[1, 1]]
        ]
    ),
    np.array(
        [
            [[ 1,  1]],
            [[ 2,  1]],
            [[ 2,  3]],
            [[ 2, 10]],
            [[ 1,  2]]
        ]
    ),
    np.array(
        [
            [[50, 100]],
            [[100, 200]]
        ]
    )
]

# seg = Segmentation.from_contour(contour_list=contours)
seg = Segmentation.from_contour(contour_list=contours, exclude_invalid_polygons=True)
logger.purple(seg)