from .field import Field, BaseField

try:
    from typing import Dict, Any, Set, Iterable, Tuple, TypeVar, Generic
except ImportError:
    from typing_extensions import Dict, Any, Set, Iterable, Tuple, TypeVar, Generic
import copy

C = TypeVar("C", bound=BaseField)


class Section(Generic[C]):
    def __init__(self, **kwargs):
        self._fields = self._build_fields()
        self.set(**kwargs)

    def _build_fields(self) -> Set[str]:
        fields: Set[str] = set()
        for attr_name in dir(self):
            try:
                attr = getattr(self, attr_name)
                if isinstance(attr, Field) or isinstance(attr, Section):
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
        return {fd_name: getattr(self, fd_name).get() for fd_name in self.field_names()}

    def __getitem__(self, field_name: str):
        return self.get_field(field_name)

    def __setitem__(self, field_name: str, field_value: Any):
        self.set(**{field_name: field_value})

    def field_names(self) -> Set[str]:
        return self._fields

    # This is just to make it look more like a dictionary.
    def items(self) -> Iterable[Tuple[str, C]]:
        for field_name in self._fields:
            yield (field_name, getattr(self, field_name))

    def keys(self) -> Iterable[str]:
        for field_name in self._fields:
            yield field_name

    def values(self) -> Iterable[C]:
        for field_name in self._fields:
            yield getattr(self, field_name)

    def get_field(self, field_name: str) -> C:
        if field_name in self._fields:
            return getattr(self, field_name)
        else:
            raise KeyError(
                "No such key {0} in {1}. Available fields are : {2}".format(
                    field_name, self.__class__.__name__, str(self.field_names())
                )
            )
