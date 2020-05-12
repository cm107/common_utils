from common_utils.common_types.point import Point2D, Point3D

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

print('Test Passed')