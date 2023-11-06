from pypharmaco.web_socket.props import SocketProps
from .section import \
  SocketSection, \
  AsyncSocketSection, \
  AsyncSocket, \
  SyncSocket
from .exceptions import WaitInput
try:
    from typing import \
        Any, \
        TypeVar, \
        List, \
        Generic, \
        Union
except ImportError:
    from typing_extensions import \
        Any, \
        TypeVar, \
        List, \
        Generic, \
        Union

U = TypeVar("U", bound = AsyncSocketSection)
T = TypeVar("T", bound = SocketSection)

def is_sys_call(content : dict) -> bool:
    return content.get('type') == 'sys_call'

def sys_call_payload(value : Any):
    return {
        'type' : 'sys_call', 
        'msg' : value
    }

def sys_call_to_reply(
    content : dict, flags : List[bool], sections : Union[List[T], List[U]]
):
    sys_call_type = content.get('msg')
    if sys_call_type == 'loop_section':
        try:
            flags_id = flags.index(False)
            return sys_call_payload(sections[flags_id].name())
        except:
            return sys_call_payload("All Sections have been passed")
    elif sys_call_type == 'section_size':
        return sys_call_payload(len(flags))
    return sys_call_payload(
        "Invalid SysCall {0}".format(sys_call_type)
    )

class SysCallSection(
    Generic[T, SyncSocket], SocketSection[SyncSocket]
):
    __slots__ = ('flags', 'sections')
    def __init__(
        self, flags : List[bool], sections : List[T]
    ):
        self.flags = flags
        self.sections = sections
    def run(self, content: dict, props: SocketProps, socket: SyncSocket):
        if is_sys_call(content):
            socket.send_json(
                sys_call_to_reply(content, self.flags, self.sections)
            )
            raise WaitInput

class AsyncSysCallSection(
    Generic[T, AsyncSocket], AsyncSocketSection[AsyncSocket]
):
    __slots__ = ('flags', 'sections')
    def __init__(
        self, flags : List[bool], sections : List[U]
    ):
        self.flags = flags
        self.sections = sections
    async def run(self, content: dict, props: SocketProps, socket: AsyncSocket):
        if is_sys_call(content):
            await socket.send_json(
                sys_call_to_reply(content, self.flags, self.sections)
            )
            raise WaitInput
    