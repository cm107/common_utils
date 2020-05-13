from logger import logger
from common_utils.common_types.point import Point2D, Point3D, Point2D_List, Point3D_List
from common_utils.common_types.keypoint import Keypoint2D, Keypoint3D, Keypoint2D_List, Keypoint3D_List

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