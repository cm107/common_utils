from typing import List
from common_utils.base.basic import MultiParameterHandler

class Test:
    def __init__(self, a: int, b: int, c: int=0):
        self.a = a
        self.b = b
        self.c = c

    @property
    def magnitude(self) -> float:
        return (self.a**2 + self.b**2 + self.c**2)**0.5

class TestHandler(MultiParameterHandler['TestHandler', 'Test']):
    def __init__(self, x: int, y: int, z: int=5, test_list: List[Test]=None):
        super().__init__(obj_type=Test, obj_list=test_list)
        self.x = x
        self.y = y
        self.z = z
        self.test_list = self.obj_list
    
    def _magnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    @property
    def magnitude(self) -> float:
        magnitude = 0
        magnitude += self._magnitude()
        for test in self:
            magnitude += test.magnitude
        return magnitude

handler = TestHandler(x=2, y=2)
handler.append(Test(a=1, b=1, c=1))
handler.append(Test(a=1, b=2, c=3))
handler.append(Test(a=0, b=0))

print(f'handler._magnitude: {handler._magnitude()}')
for i in range(len(handler)):
    print(f'handler[i].magnitude: {handler[i].magnitude}')
print(f'handler.magnitude: {handler.magnitude}')

handler[1:3] = [Test(a=2, b=2, c=2), Test(a=3, b=3, c=3)]
print('handler[1:3] = [Test(a=2, b=2, c=2), Test(a=3, b=3, c=3)]')

print(f'handler._magnitude: {handler._magnitude()}')
for i in range(len(handler)):
    print(f'handler[i].magnitude: {handler[i].magnitude}')
print(f'handler.magnitude: {handler.magnitude}')