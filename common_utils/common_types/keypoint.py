from __future__ import annotations
from typing import List
import numpy as np
from imgaug.augmentables.kps import Keypoint as ImgAug_Keypoint, KeypointsOnImage as ImgAug_Keypoints
from logger import logger
from .point import Point2D, Point3D
from ..check_utils import check_type, check_type_from_list, \
    check_value, check_list_length

class Keypoint2D:
    def __init__(self, point: Point2D, visibility: int):
        check_type(point, valid_type_list=[Point2D])
        self.point = point
        check_value(visibility, valid_value_list=[0, 1, 2])
        self.visibility = visibility

    def __str__(self) -> str:
        return f"Keypoint2D({self.point.x},{self.point.y},{self.visibility})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def buffer(self, kpt: Keypoint2D) -> Keypoint2D:
        return kpt

    def copy(self) -> Keypoint2D:
        return Keypoint2D(point=self.point, visibility=self.visibility)

    def to_list(self) -> list:
        return self.point.to_list() + [self.visibility]

    @classmethod
    def from_list(cls, val_list: list) -> Keypoint2D:
        check_list_length(val_list, correct_length=3, ineq_type='eq')
        return Keypoint2D(
            point=Point2D.from_list(val_list[:2]),
            visibility=val_list[2]
        )

    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list)

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> Keypoint2D:
        return cls.from_list(arr.tolist())

    def to_imgaug(self) -> ImgAug_Keypoint:
        return ImgAug_Keypoint(x=self.point.x, y=self.point.y)

    @classmethod
    def from_imgaug(cls, imgaug_kpt: ImgAug_Keypoint, visibility: int=2) -> Keypoint2D:
        return Keypoint2D(point=Point2D(x=imgaug_kpt.x, y=imgaug_kpt.y), visibility=visibility)

class Keypoint3D:
    def __init__(self, point: Point3D, visibility: int):
        check_type(point, valid_type_list=[Point3D])
        self.point = point
        check_value(visibility, valid_value_list=[0, 1, 2])
        self.visibility = visibility

    def __str__(self) -> str:
        return f"Keypoint3D({self.point.x},{self.point.y},{self.point.z},{self.visibility})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def buffer(self, kpt: Keypoint3D) -> Keypoint3D:
        return kpt

    def copy(self) -> Keypoint3D:
        return Keypoint3D(point=self.point, visibility=self.visibility)

    def to_list(self) -> list:
        return self.point.to_list() + [self.visibility]

    @classmethod
    def from_list(cls, val_list: list) -> Keypoint3D:
        check_list_length(val_list, correct_length=4, ineq_type='eq')
        return Keypoint3D(
            point=Point3D.from_list(val_list[:3]),
            visibility=val_list[3]
        )

    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list)

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> Keypoint3D:
        return cls.from_list(arr.tolist())

class Keypoint2D_List:
    def __init__(self, kpt_list: List[Keypoint2D]=None):
        if kpt_list is not None:
            check_type_from_list(kpt_list, valid_type_list=[Keypoint2D])
            self.kpt_list = kpt_list
        else:
            self.kpt_list = []

    def __str__(self) -> str:
        return str(self.to_list(demarcation=False))

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.kpt_list)

    def __getitem__(self, idx: int) -> Keypoint2D:
        if len(self.kpt_list) == 0:
            logger.error(f"KeyPoint2D_List is empty.")
            raise IndexError
        elif idx < 0 or idx >= len(self.kpt_list):
            logger.error(f"Index out of range: {idx}")
            raise IndexError
        else:
            return self.kpt_list[idx]

    def __setitem__(self, idx: int, value: Keypoint2D):
        check_type(value, valid_type_list=[Keypoint2D])
        self.kpt_list[idx] = value

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> Keypoint2D:
        if self.n < len(self.kpt_list):
            result = self.kpt_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @classmethod
    def buffer(self, kpt_list: Keypoint2D_List) -> Keypoint2D_List:
        return kpt_list

    def copy(self) -> Keypoint2D_List:
        return Keypoint2D_List(kpt_list=self.kpt_list.copy())

    def append(self, kpt: Keypoint2D):
        check_type(kpt, valid_type_list=[Keypoint2D])
        self.kpt_list.append(kpt)

    def to_numpy(self, demarcation: bool=False) -> np.ndarray:
        if demarcation:
            return np.array([kpt.to_list() for kpt in self])
        else:
            return np.array([kpt.to_list() for kpt in self]).reshape(-1)

    @classmethod
    def from_numpy(cls, arr: np.ndarray, demarcation: bool=False) -> Keypoint2D_List:
        if demarcation:
            if arr.shape[-1] != 3:
                logger.error(f"arr.shape[-1] != 3")
                raise Exception
            return Keypoint2D_List(
                kpt_list=[Keypoint2D.from_numpy(arr_part) for arr_part in arr]
            )
        else:
            if len(arr.shape) != 1:
                logger.error(f"Expecting flat array when demarcation=False")
                logger.error(f"arr.shape: {arr.shape}")
                raise Exception
            elif arr.shape[0] % 3 != 0:
                logger.error(f"arr.shape[0] % 3 == {arr.shape[0]} % 3 == {arr.shape[0] % 3} != 0")
                raise Exception
            return Keypoint2D_List(
                kpt_list=[Keypoint2D.from_numpy(arr_part) for arr_part in arr.reshape(-1, 3)]
            )

    def to_list(self, demarcation: bool=False) -> list:
        return self.to_numpy(demarcation=demarcation).tolist()

    @classmethod
    def from_list(cls, value_list: list, demarcation: bool=False) -> Keypoint2D_List:
        return cls.from_numpy(arr=np.array(value_list), demarcation=demarcation)

    def to_imgaug(self, img_shape: list) -> ImgAug_Keypoints:
        return ImgAug_Keypoints(
            keypoints=[kpt.to_imgaug() for kpt in self],
            shape=img_shape
        )

    @classmethod
    def from_imgaug(cls, imgaug_kpts: ImgAug_Keypoints) -> Keypoint2D_List:
        return Keypoint2D_List(
            kpt_list=[Keypoint2D.from_imgaug(imgaug_kpt) for imgaug_kpt in imgaug_kpts.keypoints]
        )

class Keypoint3D_List:
    def __init__(self, kpt_list: List[Keypoint3D]=None):
        if kpt_list is not None:
            check_type_from_list(kpt_list, valid_type_list=[Keypoint3D])
            self.kpt_list = kpt_list
        else:
            self.kpt_list = []

    def __str__(self) -> str:
        return str(self.to_list(demarcation=False))

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.kpt_list)

    def __getitem__(self, idx: int) -> Keypoint3D:
        if len(self.kpt_list) == 0:
            logger.error(f"Keypoint3D_List is empty.")
            raise IndexError
        elif idx < 0 or idx >= len(self.kpt_list):
            logger.error(f"Index out of range: {idx}")
            raise IndexError
        else:
            return self.kpt_list[idx]

    def __setitem__(self, idx: int, value: Keypoint3D):
        check_type(value, valid_type_list=[Keypoint3D])
        self.kpt_list[idx] = value

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> Keypoint3D:
        if self.n < len(self.kpt_list):
            result = self.kpt_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @classmethod
    def buffer(self, kpt_list: Keypoint3D_List) -> Keypoint3D_List:
        return kpt_list

    def copy(self) -> Keypoint3D_List:
        return Keypoint3D_List(kpt_list=self.kpt_list.copy())

    def append(self, kpt: Keypoint3D):
        check_type(kpt, valid_type_list=[Keypoint3D])
        self.kpt_list.append(kpt)

    def to_numpy(self, demarcation: bool=False) -> np.ndarray:
        if demarcation:
            return np.array([kpt.to_list() for kpt in self])
        else:
            return np.array([kpt.to_list() for kpt in self]).reshape(-1)

    @classmethod
    def from_numpy(cls, arr: np.ndarray, demarcation: bool=False) -> Keypoint3D_List:
        if demarcation:
            if arr.shape[-1] != 4:
                logger.error(f"arr.shape[-1] != 4")
                raise Exception
            return Keypoint3D_List(
                kpt_list=[Keypoint3D.from_numpy(arr_part) for arr_part in arr]
            )
        else:
            if len(arr.shape) != 1:
                logger.error(f"Expecting flat array when demarcation=False")
                logger.error(f"arr.shape: {arr.shape}")
                raise Exception
            elif arr.shape[0] % 4 != 0:
                logger.error(f"arr.shape[0] % 4 == {arr.shape[0]} % 4 == {arr.shape[0] % 4} != 0")
                raise Exception
            return Keypoint3D_List(
                kpt_list=[Keypoint3D.from_numpy(arr_part) for arr_part in arr.reshape(-1, 4)]
            )

    def to_list(self, demarcation: bool=False) -> list:
        return self.to_numpy(demarcation=demarcation).tolist()

    @classmethod
    def from_list(cls, value_list: list, demarcation: bool=False) -> Keypoint3D_List:
        return cls.from_numpy(arr=np.array(value_list), demarcation=demarcation)