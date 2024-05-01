from typing import \
  Dict, \
  Any
from typing_extensions import \
  Protocol

class JSONSocketConsumerI(Protocol):
    def send_json(self, content : Dict[str, Any]):
        raise NotImplementedError
    def close(self):
        raise NotImplementedError
    
class AsyncJSONSocketConsumerI(Protocol):
    async def send_json(self, content : Dict[str, Any]):
        raise NotImplementedError
    async def close(self):
        raise NotImplementedError
    