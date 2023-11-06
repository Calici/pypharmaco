from pypharmaco.structure import Section, Field
try:
  from typing import \
    TypeVar, \
    Generic
except ImportError:
  from typing_extensions import \
    TypeVar, \
    Generic
T = TypeVar("T")
class SocketField(Field[T], Generic[T]):
    pass

class SocketProps(Section):
    pass