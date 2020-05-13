from logger import logger
from common_utils.common_types.point import Point2D, Point3D, Point2D_List, Point3D_List
from common_utils.common_types.keypoint import Keypoint2D, Keypoint3D, Keypoint2D_List, Keypoint3D_List
from common_utils.common_types.bbox import BBox
from common_utils.common_types.segmentation import Polygon, Segmentation

const_int = 10
const_float = 20.0

pt2d_0 = Point2D(x=1.0, y=2.0)
pt2d_1 = Point2D(x=3.0, y=4.0)
assert pt2d_0 + pt2d_1 == Point2D(x=pt2d_0.x+pt2d_1.x, y=pt2d_0.y+pt2d_1.y)
assert pt2d_0 + const_int == Point2D(x=pt2d_0.x+const_int, y=pt2d_0.y+const_int)
assert pt2d_0 + const_float == Point2D(x=pt2d_0.x+const_float, y=pt2d_0.y+const_float)

assert pt2d_0 - pt2d_1 == Point2D(x=pt2d_0.x-pt2d_1.x, y=pt2d_0.y-pt2d_1.y)
assert pt2d_0 - const_int == Point2D(x=pt2d_0.x-const_int, y=pt2d_0.y-const_int)
assert pt2d_0 - const_float == Point2D(x=pt2d_0.x-const_float, y=pt2d_0.y-const_float)

assert pt2d_0 * const_int == Point2D(x=pt2d_0.x*const_int, y=pt2d_0.y*const_int)
assert pt2d_0 * const_float == Point2D(x=pt2d_0.x*const_float, y=pt2d_0.y*const_float)

assert pt2d_0 / const_int == Point2D(x=pt2d_0.x/const_int, y=pt2d_0.y/const_int)
assert pt2d_0 / const_float == Point2D(x=pt2d_0.x/const_float, y=pt2d_0.y/const_float)

pt3d_0 = Point3D(x=1.0, y=2.0, z=3.0)
pt3d_1 = Point3D(x=4.0, y=5.0, z=6.0)

print(f'Point2D Test Passed')

pt2d_list_0 = Point2D_List(point_list=[pt2d_0 for i in range(5)])

assert pt2d_list_0 + pt2d_1 == Point2D_List([point+pt2d_1 for point in pt2d_list_0])
assert pt2d_list_0 + const_int == Point2D_List([point+const_int for point in pt2d_list_0])
assert pt2d_list_0 - pt2d_1 == Point2D_List([point-pt2d_1 for point in pt2d_list_0])
assert pt2d_list_0 - const_int == Point2D_List([point-const_int for point in pt2d_list_0])
assert pt2d_list_0 * const_int == Point2D_List([point*const_int for point in pt2d_list_0])
assert pt2d_list_0 / const_int == Point2D_List([point/const_int for point in pt2d_list_0])

print(f'Point2D_List Test Passed')

assert pt3d_0 + pt3d_1 == Point3D(x=pt3d_0.x+pt3d_1.x, y=pt3d_0.y+pt3d_1.y, z=pt3d_0.z+pt3d_1.z)
assert pt3d_0 + const_int == Point3D(x=pt3d_0.x+const_int, y=pt3d_0.y+const_int, z=pt3d_0.z+const_int)
assert pt3d_0 + const_float == Point3D(x=pt3d_0.x+const_float, y=pt3d_0.y+const_float, z=pt3d_0.z+const_float)

assert pt3d_0 - pt3d_1 == Point3D(x=pt3d_0.x-pt3d_1.x, y=pt3d_0.y-pt3d_1.y, z=pt3d_0.z-pt3d_1.z)
assert pt3d_0 - const_int == Point3D(x=pt3d_0.x-const_int, y=pt3d_0.y-const_int, z=pt3d_0.z-const_int)
assert pt3d_0 - const_float == Point3D(x=pt3d_0.x-const_float, y=pt3d_0.y-const_float, z=pt3d_0.z-const_float)

assert pt3d_0 * const_int == Point3D(x=pt3d_0.x*const_int, y=pt3d_0.y*const_int, z=pt3d_0.z*const_int)
assert pt3d_0 * const_float == Point3D(x=pt3d_0.x*const_float, y=pt3d_0.y*const_float, z=pt3d_0.z*const_float)

assert pt3d_0 / const_int == Point3D(x=pt3d_0.x/const_int, y=pt3d_0.y/const_int, z=pt3d_0.z/const_int)
assert pt3d_0 / const_float == Point3D(x=pt3d_0.x/const_float, y=pt3d_0.y/const_float, z=pt3d_0.z/const_float)

print(f'Point3D Test Passed')

pt3d_list_0 = Point3D_List(point_list=[pt3d_0 for i in range(5)])

assert pt3d_list_0 + pt3d_1 == Point3D_List([point+pt3d_1 for point in pt3d_list_0])
assert pt3d_list_0 + const_int == Point3D_List([point+const_int for point in pt3d_list_0])
assert pt3d_list_0 - pt3d_1 == Point3D_List([point-pt3d_1 for point in pt3d_list_0])
assert pt3d_list_0 - const_int == Point3D_List([point-const_int for point in pt3d_list_0])
assert pt3d_list_0 * const_int == Point3D_List([point*const_int for point in pt3d_list_0])
assert pt3d_list_0 / const_int == Point3D_List([point/const_int for point in pt3d_list_0])

print(f'Point3D_List Test Passed')

kpt2d_0 = Keypoint2D(point=pt2d_0.copy(), visibility=2)
kpt2d_1 = Keypoint2D(point=pt2d_1.copy(), visibility=2)

assert kpt2d_0 + pt2d_1 == Keypoint2D(point=kpt2d_0.point+pt2d_1, visibility=kpt2d_0.visibility)
assert kpt2d_0 + const_int == Keypoint2D(point=kpt2d_0.point+const_int, visibility=kpt2d_0.visibility)
assert kpt2d_0 + kpt2d_1 == Keypoint2D(point=kpt2d_0.point+kpt2d_1.point, visibility=int(max(kpt2d_0.visibility, kpt2d_1.visibility)))
assert kpt2d_0 - pt2d_1 == Keypoint2D(point=kpt2d_0.point-pt2d_1, visibility=kpt2d_0.visibility)
assert kpt2d_0 - const_int == Keypoint2D(point=kpt2d_0.point-const_int, visibility=kpt2d_0.visibility)
assert kpt2d_0 - kpt2d_1 == Keypoint2D(point=kpt2d_0.point-kpt2d_1.point, visibility=int(max(kpt2d_0.visibility, kpt2d_1.visibility)))
assert kpt2d_0 * const_int == Keypoint2D(point=kpt2d_0.point*const_int, visibility=kpt2d_0.visibility)
assert kpt2d_0 / const_int == Keypoint2D(point=kpt2d_0.point/const_int, visibility=kpt2d_0.visibility)

print(f'Keypoint2D Test Passed')

kpt2d_list_0 = Keypoint2D_List(kpt_list=[kpt2d_0 for i in range(5)])

assert kpt2d_list_0 + kpt2d_1 == Keypoint2D_List([kpt+kpt2d_1 for kpt in kpt2d_list_0])
assert kpt2d_list_0 + pt2d_1 == Keypoint2D_List([kpt+pt2d_1 for kpt in kpt2d_list_0])
assert kpt2d_list_0 + const_int == Keypoint2D_List([kpt+const_int for kpt in kpt2d_list_0])
assert kpt2d_list_0 - kpt2d_1 == Keypoint2D_List([kpt-kpt2d_1 for kpt in kpt2d_list_0])
assert kpt2d_list_0 - pt2d_1 == Keypoint2D_List([kpt-pt2d_1 for kpt in kpt2d_list_0])
assert kpt2d_list_0 - const_int == Keypoint2D_List([kpt-const_int for kpt in kpt2d_list_0])
assert kpt2d_list_0 * const_int == Keypoint2D_List([kpt*const_int for kpt in kpt2d_list_0])
assert kpt2d_list_0 / const_int == Keypoint2D_List([kpt/const_int for kpt in kpt2d_list_0])

print(f'Keypoint2D_List Test Passed')

kpt3d_0 = Keypoint3D(point=pt3d_0.copy(), visibility=2)
kpt3d_1 = Keypoint3D(point=pt3d_1.copy(), visibility=2)

assert kpt3d_0 + pt3d_1 == Keypoint3D(point=kpt3d_0.point+pt3d_1, visibility=kpt3d_0.visibility)
assert kpt3d_0 + const_int == Keypoint3D(point=kpt3d_0.point+const_int, visibility=kpt3d_0.visibility)
assert kpt3d_0 + kpt3d_1 == Keypoint3D(point=kpt3d_0.point+kpt3d_1.point, visibility=int(max(kpt3d_0.visibility, kpt3d_1.visibility)))
assert kpt3d_0 - pt3d_1 == Keypoint3D(point=kpt3d_0.point-pt3d_1, visibility=kpt3d_0.visibility)
assert kpt3d_0 - const_int == Keypoint3D(point=kpt3d_0.point-const_int, visibility=kpt3d_0.visibility)
assert kpt3d_0 - kpt3d_1 == Keypoint3D(point=kpt3d_0.point-kpt3d_1.point, visibility=int(max(kpt3d_0.visibility, kpt3d_1.visibility)))
assert kpt3d_0 * const_int == Keypoint3D(point=kpt3d_0.point*const_int, visibility=kpt3d_0.visibility)
assert kpt3d_0 / const_int == Keypoint3D(point=kpt3d_0.point/const_int, visibility=kpt3d_0.visibility)

print(f'Keypoint3D Test Passed')

kpt3d_list_0 = Keypoint3D_List(kpt_list=[kpt3d_0 for i in range(5)])

assert kpt3d_list_0 + kpt3d_1 == Keypoint3D_List([kpt+kpt3d_1 for kpt in kpt3d_list_0])
assert kpt3d_list_0 + pt3d_1 == Keypoint3D_List([kpt+pt3d_1 for kpt in kpt3d_list_0])
assert kpt3d_list_0 + const_int == Keypoint3D_List([kpt+const_int for kpt in kpt3d_list_0])
assert kpt3d_list_0 - kpt3d_1 == Keypoint3D_List([kpt-kpt3d_1 for kpt in kpt3d_list_0])
assert kpt3d_list_0 - pt3d_1 == Keypoint3D_List([kpt-pt3d_1 for kpt in kpt3d_list_0])
assert kpt3d_list_0 - const_int == Keypoint3D_List([kpt-const_int for kpt in kpt3d_list_0])
assert kpt3d_list_0 * const_int == Keypoint3D_List([kpt*const_int for kpt in kpt3d_list_0])
assert kpt3d_list_0 / const_int == Keypoint3D_List([kpt/const_int for kpt in kpt3d_list_0])

print(f'Keypoint3D_List Test Passed')

bbox0 = BBox(xmin=0, ymin=1, xmax=2, ymax=3)
bbox1 = BBox(xmin=4, ymin=5, xmax=6, ymax=7)
assert bbox0 + bbox1 == BBox(xmin=0, ymin=1, xmax=6, ymax=7)
assert bbox0 + const_int == BBox(xmin=bbox0.xmin+const_int, ymin=bbox0.ymin+const_int, xmax=bbox0.xmax+const_int, ymax=bbox0.ymax+const_int)
assert bbox0 + const_float == BBox(xmin=bbox0.xmin+const_float, ymin=bbox0.ymin+const_float, xmax=bbox0.xmax+const_float, ymax=bbox0.ymax+const_float)
assert bbox0 + pt2d_0 == BBox(xmin=bbox0.xmin+pt2d_0.x, ymin=bbox0.ymin+pt2d_0.y, xmax=bbox0.xmax+pt2d_0.x, ymax=bbox0.ymax+pt2d_0.y)
assert bbox0 + kpt2d_0 == BBox(xmin=bbox0.xmin+kpt2d_0.point.x, ymin=bbox0.ymin+kpt2d_0.point.y, xmax=bbox0.xmax+kpt2d_0.point.x, ymax=bbox0.ymax+kpt2d_0.point.y)

assert bbox0 - const_int == BBox(xmin=bbox0.xmin-const_int, ymin=bbox0.ymin-const_int, xmax=bbox0.xmax-const_int, ymax=bbox0.ymax-const_int)
assert bbox0 - const_float == BBox(xmin=bbox0.xmin-const_float, ymin=bbox0.ymin-const_float, xmax=bbox0.xmax-const_float, ymax=bbox0.ymax-const_float)
assert bbox0 - pt2d_0 == BBox(xmin=bbox0.xmin-pt2d_0.x, ymin=bbox0.ymin-pt2d_0.y, xmax=bbox0.xmax-pt2d_0.x, ymax=bbox0.ymax-pt2d_0.y)
assert bbox0 - kpt2d_0 == BBox(xmin=bbox0.xmin-kpt2d_0.point.x, ymin=bbox0.ymin-kpt2d_0.point.y, xmax=bbox0.xmax-kpt2d_0.point.x, ymax=bbox0.ymax-kpt2d_0.point.y)

assert bbox0 * const_int == BBox(xmin=bbox0.xmin*const_int, ymin=bbox0.ymin*const_int, xmax=bbox0.xmax*const_int, ymax=bbox0.ymax*const_int)
assert bbox0 * const_float == BBox(xmin=bbox0.xmin*const_float, ymin=bbox0.ymin*const_float, xmax=bbox0.xmax*const_float, ymax=bbox0.ymax*const_float)

assert bbox0 / const_int == BBox(xmin=bbox0.xmin/const_int, ymin=bbox0.ymin/const_int, xmax=bbox0.xmax/const_int, ymax=bbox0.ymax/const_int)
assert bbox0 / const_float == BBox(xmin=bbox0.xmin/const_float, ymin=bbox0.ymin/const_float, xmax=bbox0.xmax/const_float, ymax=bbox0.ymax/const_float)

print('BBox Test Passed')

poly2d_0 = Polygon.from_point2d_list(
    Point2D_List(
        [
            Point2D(0,0), Point2D(2,0), Point2D(2,3), Point2D(1, 1)
        ]
    )
)
poly2d_1 = Polygon.from_point2d_list(
    Point2D_List(
        [
            Point2D(0,10), Point2D(2,10), Point2D(2,13), Point2D(1, 11)
        ]
    )
)
poly2d_2 = Polygon.from_point2d_list(
    Point2D_List(
        [
            Point2D(0,20), Point2D(2,20), Point2D(2,23), Point2D(1, 21)
        ]
    )
)
poly3d_0 = Polygon.from_point3d_list(
    Point3D_List(
        [
            Point3D(0,0,0), Point3D(2,0,1), Point3D(2,3,0), Point3D(1, 1,1)
        ]
    )
)

assert poly2d_0 + kpt2d_0 == Polygon.from_point2d_list(Point2D_List([point+kpt2d_0.point for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 + kpt3d_0 == Polygon.from_point3d_list(Point3D_List([point+kpt3d_0.point for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 + pt2d_0 == Polygon.from_point2d_list(Point2D_List([point+pt2d_0 for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 + pt3d_0 == Polygon.from_point3d_list(Point3D_List([point+pt3d_0 for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 + const_float == Polygon.from_point2d_list(Point2D_List([point+const_float for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 + const_float == Polygon.from_point3d_list(Point3D_List([point+const_float for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 + const_int == Polygon.from_point2d_list(Point2D_List([point+const_int for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 + const_int == Polygon.from_point3d_list(Point3D_List([point+const_int for point in poly3d_0.to_point3d_list()]))

assert poly2d_0 - kpt2d_0 == Polygon.from_point2d_list(Point2D_List([point-kpt2d_0.point for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 - kpt3d_0 == Polygon.from_point3d_list(Point3D_List([point-kpt3d_0.point for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 - pt2d_0 == Polygon.from_point2d_list(Point2D_List([point-pt2d_0 for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 - pt3d_0 == Polygon.from_point3d_list(Point3D_List([point-pt3d_0 for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 - const_float == Polygon.from_point2d_list(Point2D_List([point-const_float for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 - const_float == Polygon.from_point3d_list(Point3D_List([point-const_float for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 - const_int == Polygon.from_point2d_list(Point2D_List([point-const_int for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 - const_int == Polygon.from_point3d_list(Point3D_List([point-const_int for point in poly3d_0.to_point3d_list()]))

assert poly2d_0 * const_float == Polygon.from_point2d_list(Point2D_List([point*const_float for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 * const_float == Polygon.from_point3d_list(Point3D_List([point*const_float for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 * const_int == Polygon.from_point2d_list(Point2D_List([point*const_int for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 * const_int == Polygon.from_point3d_list(Point3D_List([point*const_int for point in poly3d_0.to_point3d_list()]))

assert poly2d_0 / const_float == Polygon.from_point2d_list(Point2D_List([point/const_float for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 / const_float == Polygon.from_point3d_list(Point3D_List([point/const_float for point in poly3d_0.to_point3d_list()]))
assert poly2d_0 / const_int == Polygon.from_point2d_list(Point2D_List([point/const_int for point in poly2d_0.to_point2d_list()]))
assert poly3d_0 / const_int == Polygon.from_point3d_list(Point3D_List([point/const_int for point in poly3d_0.to_point3d_list()]))

print('Polygon Test Passed')

seg0 = Segmentation([poly2d_0, poly2d_1])
seg1 = Segmentation([poly2d_2])

assert seg0 + seg1 == Segmentation(seg0.polygon_list + seg1.polygon_list)
assert seg0 + pt2d_0 == Segmentation([poly + pt2d_0 for poly in seg0])
assert seg0 + kpt2d_0 == Segmentation([poly + kpt2d_0 for poly in seg0])
assert seg0 + const_int == Segmentation([poly + const_int for poly in seg0])
assert seg0 + const_float == Segmentation([poly + const_float for poly in seg0])

assert seg0 - pt2d_0 == Segmentation([poly - pt2d_0 for poly in seg0])
assert seg0 - kpt2d_0 == Segmentation([poly - kpt2d_0 for poly in seg0])
assert seg0 - const_int == Segmentation([poly - const_int for poly in seg0])
assert seg0 - const_float == Segmentation([poly - const_float for poly in seg0])

assert seg0 * const_int == Segmentation([poly * const_int for poly in seg0])
assert seg0 * const_float == Segmentation([poly * const_float for poly in seg0])

assert seg0 / const_int == Segmentation([poly / const_int for poly in seg0])
assert seg0 / const_float == Segmentation([poly / const_float for poly in seg0])

print('Segmentation Test Passed')