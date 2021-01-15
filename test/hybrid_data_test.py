from __future__ import annotations
from typing import List
from common_utils.base.prediction import HybridData, HybridDatum, \
    PredictionData, PredictionDatum, GTData, GTDatum
from common_utils.base.basic import BasicLoadableObject, BasicLoadableHandler, BasicHandler

class GT_Distance(
    GTDatum['GT_Distance'],
    BasicLoadableObject['GT_Distance']
):
    def __init__(self, frame: str, test_name: str, distance: float):
        super().__init__(frame=frame, test_name=test_name)
        self.distance = distance

class GT_Distance_List(
    GTData['GT_Distance_List', 'GT_Distance'],
    BasicLoadableHandler['GT_Distance_List', 'GT_Distance'],
    BasicHandler['GT_Distance_List', 'GT_Distance']
):
    def __init__(self, obj_list: List[GT_Distance]=None):
        super().__init__(obj_type=GT_Distance, obj_list=obj_list)

    @classmethod
    def from_dict_list(cls, dict_list: List[dict]) -> GT_Distance_List:
        return GT_Distance_List([GT_Distance.from_dict(item_dict) for item_dict in dict_list])

class DT_Distance(
    PredictionDatum['DT_Distance'],
    BasicLoadableObject['DT_Distance']
):
    def __init__(self, frame: str, test_name: str, model_name: str, distance: float):
        super().__init__(frame=frame, test_name=test_name, model_name=model_name)
        self.distance = distance

class DT_Distance_List(
    PredictionData['DT_Distance_List', 'DT_Distance'],
    BasicLoadableHandler['DT_Distance_List', 'DT_Distance'],
    BasicHandler['DT_Distance_List', 'DT_Distance']
):
    def __init__(self, obj_list: List[DT_Distance]=None):
        super().__init__(obj_type=DT_Distance, obj_list=obj_list)

class DistanceError(
    HybridDatum['DistanceError'],
    BasicLoadableObject['DistanceError']
):
    def __init__(self, frame: str, test_name: str, model_name: str, error: float):
        super().__init__(frame=frame, test_name=test_name, model_name=model_name)
        self.error = error

    @classmethod
    def from_gtdt(cls, gt: GT_Distance, dt: DT_Distance, fallback_model_name: str=None, always_positive: bool=True) -> DistanceError:
        if dt is not None:
            error = dt.distance - gt.distance
        else:
            error = None
        return DistanceError(
            frame=gt.frame, test_name=gt.test_name, model_name=fallback_model_name,
            error=abs(error) if always_positive else error
        )

class DistanceErrorList(
    HybridData['DistanceErrorList', 'DistanceError'],
    BasicLoadableHandler['DistanceErrorList', 'DistanceError'],
    BasicHandler['DistanceErrorList', 'DistanceError']
):
    def __init__(self, obj_list: List[DistanceError]=None):
        super().__init__(obj_type=DistanceError, obj_list=obj_list)
    
    @classmethod
    def from_dict_list(cls, dict_list: List[dict]) -> DistanceErrorList:
        return DistanceErrorList([DistanceError.from_dict(item_dict) for item_dict in dict_list])

gt, dt = GT_Distance_List(), DT_Distance_List()
test_name = 'test_0'
for i in range(10):
    frame = f'{i}.jpg'
    gt.append(GT_Distance(frame=frame, test_name=test_name, distance=i))
    dt.append(DT_Distance(frame=frame, test_name=test_name, model_name=f'model_{i}', distance=i+(0.1*i*((-1)**i))))
test_name = 'test_1'
for i in range(10):
    frame = f'{i}.jpg'
    j = i**2
    gt.append(GT_Distance(frame=frame, test_name=test_name, distance=j))
    dt.append(DT_Distance(frame=frame, test_name=test_name, model_name=f'model_{i}', distance=j+(0.1*i*((-1)**i))))
test_name = 'test_2'
for i in range(10):
    frame = f'{i}.jpg'
    j = i**3
    gt.append(GT_Distance(frame=frame, test_name=test_name, distance=j))
    dt.append(DT_Distance(frame=frame, test_name=test_name, model_name=f'model_{i}', distance=j+(0.1*i*((-1)**i))))

print(f'gt:\n{gt}')
print(f'dt:\n{dt}')
error = DistanceErrorList.from_gtdt(gt=gt, dt=dt, obj_type=DistanceError, always_positive=False)
print(error)