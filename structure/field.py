from typing import \
  TypeVar, \
  Generic, \
  Union, \
  Type, \
  Any

T = TypeVar("T")
class Field(Generic[T]):
    __slots__ = ("type", 'value', 'default')
    def __init__(self, 
        type : Union[Type[T], None] = None, default : T = None
    ):
        self.type   = type
        self.default= default
        self.reset()
    def validate(self, value : Any) -> T:
        if self.type is not None:
            try:
                if isinstance(value, self.type): return value
                return self.type(value)
            except: 
                raise TypeError(f"{value} cannot be converted to {self.type}")
        return value
    def set(self, value : T):
        value   = self.validate(value)
        self.value = value
        return self.value
    def get(self) -> T:
        return self.value
    def reset(self):
        self.value = self.default