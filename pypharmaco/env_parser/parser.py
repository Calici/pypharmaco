import os
import pathlib
try:
    from typing import \
        Callable, \
        Union, \
        Any, \
        List, \
        TypedDict
except ImportError:
    from typing_extensions import \
        Callable, \
        Union, \
        Any, \
        List, \
        TypedDict
from .exceptions import EnvParserError
    
class EnvEntry(TypedDict):
    name : str
    is_secret : bool
    default_value : Union[str, None]
    parser : Union[Callable[[str], Any], None]

def create_entry(
    name : str, 
    is_secret : bool = False, 
    default_value : Union[str, None] = None, 
    parser : Union[Callable[[str], Any], None] = None
) -> EnvEntry:
    return {
        'name' : name, 
        'is_secret' : is_secret, 
        'default_value' : default_value, 
        'parser' : parser
    }

class EnvParser:
    __slots__ = ('env_fields', 'is_production')
    def __init__(self, fields : List[EnvEntry]):
        self.is_production = os.environ.get('PRODUCTION', 'false') == 'true'
        self.env_fields = {
            field["name"] : self.parse_field(field) for field in fields
        }

    def get(self, key : str) -> Any:
        return self.env_fields[key]
        
    def parse_field(self, field : EnvEntry):
        env_value = os.environ.get(field["name"], field["default_value"])
        if env_value is None:
            raise EnvParserError(
                "Env with key {0} does not exist".format(field["name"])
            )
        if self.is_production and field["is_secret"]:
            value = self.from_secret_file(pathlib.Path(env_value))
        else:
            value = env_value
        if field["parser"] is not None:
            return field["parser"](value)
        return value
    
    def from_secret_file(self, path : pathlib.Path) -> str:
        with open(path, 'r') as f:
            return f.read()