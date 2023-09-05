from __future__ import annotations
from typing import \
  TypeVar, \
  Generic, \
  Union, \
  Type, \
  Protocol

T = TypeVar("T")
class BaseField(Generic[T], Protocol):
    def validate(self, value : Union[T, str]) -> T:
        ...
    def get(self) -> T:
        ...
    def set(self, value : Union[T, str]):
        ...

class Field(Generic[T], BaseField[T]):
    __slots__ = ("type", 'value', 'default', 'allow_none')
    def __init__(self, 
        type : Union[Type[T], None] = None, default : T = None, 
        allow_none : bool = True
    ):
        self.type = type
        self.default = default
        self.allow_none = allow_none
        self.set(default)

    def validate(self, value : Union[T, str]) -> T:
        if self.type is not None:
            try:
                if self.allow_none and value is None:
                    return value
                elif isinstance(value, str): 
                    return self.type(str)
                else:
                    return value
            except: 
                raise TypeError(f"{value} cannot be converted to {self.type}")
        return value #type: ignore [Assume Programmer knows what they are doing]
    
    def set(self, value : T):
        value   = self.validate(value)
        self.value = value
        return self.value
    
    def get(self) -> T:
        return self.value