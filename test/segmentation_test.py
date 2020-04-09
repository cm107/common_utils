from logger import logger
from common_utils.common_types.segmentation import Segmentation, Polygon

seg = Segmentation(
    [
        Polygon.from_list(
            points=[
                [0, 0], [1, 0], [1, 2], [0, 1]
            ],
            dimensionality=2,
            demarcation=True
        ),
        Polygon.from_list(
            points=[
                [0.5, 0], [1.5, 0], [1.5, 2], [0.5, 1]
            ],
            dimensionality=2,
            demarcation=True
        ),
        Polygon.from_list(
            points=[
                [1, 0], [2, 0], [2, 2], [1, 1]
            ],
            dimensionality=2,
            demarcation=True
        ),
        Polygon.from_list(
            points=[
                [1, 1], [2, 1], [2, 3], [2, 10], [1, 2]
            ],
            dimensionality=2,
            demarcation=True
        )
    ]
)
for poly in seg:
    new_points = []
    for val in poly.points:
        new_val = 100 * val
        new_points.append(new_val)
    poly.points = new_points

logger.purple(f'seg:\n{seg}')
logger.purple(f'seg.to_bbox():\n{seg.to_bbox()}')
logger.purple(f'seg.area():\n{seg.area()}')
logger.purple(f'seg.centroid():\n{seg.centroid()}')
logger.purple(f'seg.within(seg.to_bbox()): {seg.within(seg.to_bbox())}')

from common_utils.cv_drawing_utils import draw_segmentation, cv_simple_image_viewer
import numpy as np

seg_bbox = seg.to_bbox()
seg_bbox_h, seg_bbox_w = seg_bbox.shape()
blank_frame = np.zeros(shape=[seg_bbox_h, seg_bbox_w, 3])
vis = draw_segmentation(img=blank_frame, segmentation=seg)
quit_flag = cv_simple_image_viewer(img=vis, preview_width=1000)