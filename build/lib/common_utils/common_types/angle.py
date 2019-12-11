import math
from common_utils.check_utils import check_type_from_list
from common_utils.common_types.constants import number_types

class EulerAngle:
    def __init__(self, roll, pitch, yaw):
        check_type_from_list(item_list=[roll, pitch, yaw], valid_type_list=number_types)
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def __str__(self) -> str:
        return f"EulerAngle({self.roll},{self.pitch},{self.yaw})"

    def __repr__(self) -> str:
        return self.__str__()

    def to_list(self) -> list:
        return [self.roll, self.pitch, self.yaw]

    @classmethod
    def from_list(self, val_list: list):
        roll, pitch, yaw = val_list
        return EulerAngle(roll=roll, pitch=pitch, yaw=yaw)

    def to_quaternion(self):
        cy = math.cos(self.yaw * 0.5)
        sy = math.sin(self.yaw * 0.5)
        cp = math.cos(self.pitch * 0.5)
        sp = math.sin(self.pitch * 0.5)
        cr = math.cos(self.roll * 0.5)
        sr = math.sin(self.roll * 0.5)

        qw = cy * cp * cr + sy * sp * sr
        qx = cy * cp * sr - sy * sp * cr
        qy = sy * cp * sr + cy * sp * cr
        qz = sy * cp * cr - cy * sp * sr

        return Quaternion(qw=qw, qx=qx, qy=qy, qz=qz)

    def to_deg_list(self) -> list:
        return [val * 180 / math.pi for val in self.to_list()]

class Quaternion:
    def __init__(self, qw, qx, qy, qz):
        check_type_from_list(item_list=[qw, qx, qy, qz], valid_type_list=number_types)
        self.qw = qw
        self.qx = qx
        self.qy = qy
        self.qz = qz

    def __str__(self) -> str:
        return f"Quaternion({self.qw},{self.qx},{self.qy},{self.qz})"

    def __repr__(self) -> str:
        return self.__str__()

    def to_list(self) -> list:
        return [self.qw, self.qx, self.qy, self.qz]

    @classmethod
    def from_list(self, val_list: list):
        qw, qx, qy, qz = val_list
        return Quaternion(qw=qw, qx=qx, qy=qy, qz=qz)

    def to_euler(self):
        # roll
        sinr_cosp = 2 * (self.qw * self.qx + self.qy * self.qz)
        cosr_cosp = 1 - 2 * (self.qx * self.qx + self.qy * self.qy)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # pitch
        sinp = 2 * (self.qw * self.qy - self.qz * self.qx)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp) # 90deg when out of range
        else:
            pitch = math.asin(sinp)

        # yaw
        siny_cosp = 2 * (self.qw * self.qz + self.qx * self.qy)
        cosy_cosp = 1 - 2 * (self.qy * self.qy + self.qz * self.qz)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return EulerAngle(roll=roll, pitch=pitch, yaw=yaw)