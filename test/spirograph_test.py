from math import pi
from common_utils.cv_drawing_utils import Spirograph, cv_simple_image_viewer

spirograph = Spirograph(r=200, partitions=12, nodes=[0, pi/2, pi, 3*pi/2])
quit_flag = cv_simple_image_viewer(img=spirograph.sample(), preview_width=1000)