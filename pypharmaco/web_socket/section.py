from .consumer import JSONSocketConsumerI, AsyncJSONSocketConsumerI
from .props import SocketProps

try:
    from typing import \
        TypeVar, \
        Generic
except ImportError:
    from typing_extensions import \
        TypeVar, \
        Generic

AsyncSocket = TypeVar('AsyncSocket', bound = AsyncJSONSocketConsumerI)
SyncSocket = TypeVar('SyncSocket', bound = JSONSocketConsumerI)
Props = TypeVar("Props", bound = SocketProps)

class NamedSection:
    def name(self):
        return self.__class__.__name__

class AsyncSocketSection(NamedSection, Generic[AsyncSocket]):
    async def run(self, 
        content : dict, props : SocketProps, socket : AsyncSocket
    ):
        pass
    async def pre_run(self, 
        content : dict, props : SocketProps, socket : AsyncSocket
    ):
        pass
    async def post_run(self, 
        content : dict, props : SocketProps, socket : AsyncSocket
    ):
        pass

class SocketSection(NamedSection, Generic[SyncSocket]):
    def run(self, 
        content : dict, props : SocketProps, socket : SyncSocket
    ): pass
    def pre_run(self, 
        content : dict, props : SocketProps, socket : SyncSocket
    ): pass
    def post_run(self, 
        content : dict, props : SocketProps, socket : SyncSocket
    ): pass