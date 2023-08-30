from .field import Field
from typing import \
  Dict, \
  Any, \
  Set
import copy

class Section(Field[Dict[str, Any]]):
    def __init__(self, **kwargs):
        self._fields = self._build_fields()
    
    def _build_fields(self) -> Set[str]:
        fields : Set[str] = set()
        for attr_name in dir(self):
            try:
                attr = getattr(self, attr_name)
                if isinstance(attr, Field):
                    setattr(self, attr_name, copy.deepcopy(attr))
                    fields.add(attr_name)
            except AttributeError:
                continue
        return fields

    def set(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._fields:
                field = getattr(self, k)
                field.set(v)

    def get(self) -> Dict[str, Any]:
        return {
            fd_name : getattr(self, fd_name).get() 
            for fd_name in self.field_names()
        }
    
    def __getitem__(self, field_name : str):
        if field_name in self._fields:
            return getattr(self, field_name)
        raise RuntimeError("No such field {0}".format(field_name))

    def __setitem__(self, field_name : str, field_value : Any):
        self.set(**{field_name : field_value})

    def field_names(self) -> Set[str]:
        return self._fields