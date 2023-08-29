from pypharmaco.structure import Section, Field
from typing import \
  TypeVar, \
  Generic

T = TypeVar("T")
class SocketField(Field[T], Generic[T]):
    pass

class SocketProps(Section):
    pass