from .consumer import JSONSocketConsumerI, AsyncJSONSocketConsumerI
from .props import SocketProps
from .exceptions import \
    SectionError, \
    WaitInput, \
    WaitInputForNext, \
    SkipCurrent, \
    SkipCurrentNoReturn, \
    SkipNextNoReturn, \
    Disconnect
from typing import \
  TypeVar, \
  Generic, \
  List
import logging

AsyncSocket = TypeVar('AsyncSocket', bound = AsyncJSONSocketConsumerI)
SyncSocket = TypeVar('SyncSocket', bound = JSONSocketConsumerI)
Props = TypeVar("Props", bound = SocketProps)


class AsyncSocketSection(Generic[AsyncSocket]):
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
    def name(self):
        return self.__class__.__name__

class SocketSection(Generic[SyncSocket]):
    def run(self, 
        content : dict, props : SocketProps, socket : SyncSocket
    ): pass
    def pre_run(self, 
        content : dict, props : SocketProps, socket : SyncSocket
    ): pass
    def post_run(self, 
        content : dict, props : SocketProps, socket : SyncSocket
    ): pass
    def name(self):
        return self.__class__.__name__

class WebSocketLoop(Generic[Props, SyncSocket]):
    __slots__ = ( 'flags', 'props', 'socket' )
    sections : List[SocketSection[SyncSocket]] = []
    def __init__(self, socket : SyncSocket, props : Props):
        self.flags = [ False for section in self.sections ]
        self.props = props
        self.socket = socket

    def run(self, content : dict):
        run_next_section = True
        for i in range(len(self.sections)):
            section = self.sections[i]
            if not run_next_section:
                self.set_flag(i, True)
                run_next_section = False
                continue
            if not self.flags[i]:
                try:
                    section.pre_run(content, self.props, self.socket)
                    section.run(content, self.props, self.socket)
                    section.post_run(content, self.props, self.socket)
                except SectionError as e:
                    self.socket.send_json({'type' : 'err', 'msg' : e.message})
                    logging.error(e.message)
                    self.socket.close()
                    break
                except WaitInput as e: break
                except WaitInputForNext: 
                    self.set_flag(i, True)
                    break
                except SkipCurrent as e: continue
                except Disconnect as e: self.socket.close()
                except SkipCurrentNoReturn:
                    self.set_flag(i, True)
                    continue
                except SkipNextNoReturn as e:
                    run_next_section = False
                    self.set_flag(i, True)
                    continue
                self.set_flag(i, True)

    def set_flag(self, idx : int, value : bool):
        self.flags[idx] = value
    
    # Ran before any connection into the websocket
    def pre_run(self):
        pass

    # Ran when connection is closed. 
    def post_run(self):
        pass

class AsyncWebSocketLoop(Generic[AsyncSocket, Props]):
    __slots__ = ( 'flags', 'props', 'socket' )
    sections : List[AsyncSocketSection[AsyncSocket]] = []
    def __init__(self, socket : AsyncSocket, props : Props):
        self.flags = [ False for section in self.sections ]
        self.props = props
        self.socket = socket

    async def run(self, content : dict):
        run_next_section = True
        for i in range(len(self.sections)):
            section = self.sections[i]
            if not run_next_section:
                self.set_flag(i, True)
                run_next_section = False
                continue
            if not self.flags[i]:
                try:
                    await section.pre_run(content, self.props, self.socket)
                    await section.run(content, self.props, self.socket)
                    await section.post_run(content, self.props, self.socket)
                except SectionError as e:
                    await self.socket.send_json(
                        {'type' : 'err', 'msg' : e.message}
                    )
                    logging.error(e.message)
                    await self.socket.close()
                    break
                except WaitInput as e: break
                except SkipCurrent as e: continue
                except Disconnect as e: await self.socket.close()
                except SkipCurrentNoReturn:
                    self.set_flag(i, True)
                    continue
                except SkipNextNoReturn as e:
                    run_next_section = False
                    self.set_flag(i, True)
                    continue
                self.set_flag(i, True)

    def set_flag(self, idx : int, value : bool):
        self.flags[idx] = value
    
    # Ran before any connection into the websocket
    async def pre_run(self):
        pass

    # Ran when connection is closed. 
    async def post_run(self):
        pass
