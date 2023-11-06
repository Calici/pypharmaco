from .consumer import JSONSocketConsumerI, AsyncJSONSocketConsumerI
from .props import SocketProps
from .section import SocketSection, AsyncSocketSection
from .exceptions import \
    SectionError, \
    WaitInputForNext, \
    SkipCurrentNoReturn, \
    SkipNextNoReturn, \
    Disconnect, \
    JumpSection, \
    SocketException, \
    ContinueLoop, \
    BreakLoop, \
    PassLoop
from .sys_call import \
    SysCallSection, \
    AsyncSysCallSection
import logging

try:
    from typing import \
        TypeVar, \
        Generic, \
        List
except ImportError:
    from typing_extensions import \
        TypeVar, \
        Generic, \
        List

AsyncSocket = TypeVar('AsyncSocket', bound = AsyncJSONSocketConsumerI)
SyncSocket = TypeVar(
    'SyncSocket', bound = JSONSocketConsumerI, covariant = True
)
Props = TypeVar("Props", bound = SocketProps)

class WebSocketLoop(Generic[Props, SyncSocket]):
    __slots__ = ( 'flags', 'props', 'socket', 'sys_call')
    sections : List[SocketSection[SyncSocket]] = []
    def __init__(self, socket : SyncSocket, props : Props):
        self.flags = [ False for section in self.sections ]
        self.props = props
        self.socket = socket
        self.sys_call = SysCallSection(self.flags, self.sections)
    
    def action_handler(self, content : dict, i : int, e : SocketException):
        if isinstance(e, WaitInputForNext):
            self.set_flag(i, True)
        elif isinstance(e, SectionError):
            self.socket.send_json({'type' : 'err', 'msg' : e.message})
            logging.error(e.message)
            self.socket.close()
        elif isinstance(e, WaitInputForNext):
            self.set_flag(i, True)
        elif isinstance(e, Disconnect):
            self.socket.close()
        elif isinstance(e, SkipCurrentNoReturn):
            self.set_flag(i, True)
        elif isinstance(e, SkipNextNoReturn):
            self.set_flag(i, True)
            if (i + 1) < len(self.sections):
                self.set_flag(i + 1, True)
        elif isinstance(e, Disconnect):
            self.socket.close()
        elif isinstance(e, JumpSection):
            target = e.target
            if e.set_flag:
                self.flags = [
                    i < target for i in range(len(self.flags)) 
                ]
            self.run(content)
        e.throw_exec()

    def run_sys_call(self, content : dict):
        # Run Sys Call First
        self.sys_call.run(content, self.props, self.socket)
        self.sys_call.pre_run(content, self.props, self.socket)
        self.sys_call.post_run(content, self.props, self.socket)

    def run(self, content : dict):
        for i in range(len(self.sections)):
            section = self.sections[i]
            if not self.flags[i]:
                try:
                    self.run_sys_call(content)
                    # Run The rest later
                    section.pre_run(content, self.props, self.socket)
                    section.run(content, self.props, self.socket)
                    section.post_run(content, self.props, self.socket)
                except Exception as e:
                    if isinstance(e, SocketException):
                        try:
                            self.action_handler(content, i, e)
                        except BreakLoop: break
                        except ContinueLoop: continue
                        except PassLoop: pass
                    else:
                        raise
                self.set_flag(i, True)
                # except SectionError as e:
                #     self.socket.send_json({'type' : 'err', 'msg' : e.message})
                #     logging.error(e.message)
                #     self.socket.close()
                #     break
                # except WaitInput as e: break
                # except WaitInputForNext: 
                #     self.set_flag(i, True)
                #     break
                # except SkipCurrent as e: continue
                # except Disconnect as e: self.socket.close()
                # except SkipCurrentNoReturn:
                #     self.set_flag(i, True)
                #     continue
                # except SkipNextNoReturn as e:
                #     run_next_section = False
                #     self.set_flag(i, True)
                #     continue
                # except JumpSection as e:
                #     target = e.target
                #     self.flags = [
                #         i < target for i in range(len(self.flags)) 
                #     ]
                #     self.run(content)

    def set_flag(self, idx : int, value : bool):
        self.flags[idx] = value
    
    # Ran before any connection into the websocket
    def pre_run(self):
        pass

    # Ran when connection is closed. 
    def post_run(self):
        pass

class AsyncWebSocketLoop(Generic[AsyncSocket, Props]):
    __slots__ = ( 'flags', 'props', 'socket', 'sys_call' )
    sections : List[AsyncSocketSection[AsyncSocket]] = []
    def __init__(self, socket : AsyncSocket, props : Props):
        self.flags = [ False for section in self.sections ]
        self.props = props
        self.socket = socket
        self.sys_call = AsyncSysCallSection(self.flags, self.sections)

    async def run_sys_call(self, content : dict):
        # Run Sys Call First
        await self.sys_call.run(content, self.props, self.socket)
        await self.sys_call.pre_run(content, self.props, self.socket)
        await self.sys_call.post_run(content, self.props, self.socket)

    async def action_handler(self, content : dict, i : int, e : SocketException):
        if isinstance(e, WaitInputForNext):
            self.set_flag(i, True)
        elif isinstance(e, SectionError):
            await self.socket.send_json({'type' : 'err', 'msg' : e.message})
            logging.error(e.message)
            await self.socket.close()
        elif isinstance(e, WaitInputForNext):
            self.set_flag(i, True)
        elif isinstance(e, Disconnect):
            await self.socket.close()
        elif isinstance(e, SkipCurrentNoReturn):
            self.set_flag(i, True)
        elif isinstance(e, SkipNextNoReturn):
            self.set_flag(i, True)
            if (i + 1) < len(self.sections):
                self.set_flag(i + 1, True)
        elif isinstance(e, Disconnect):
            await self.socket.close()
        elif isinstance(e, JumpSection):
            target = e.target
            if e.set_flag:
                self.flags = [
                    i < target for i in range(len(self.flags)) 
                ]
            await self.run(content)
        e.throw_exec()

    async def run(self, content : dict):
        for i in range(len(self.sections)):
            section = self.sections[i]
            if not self.flags[i]:
                try:
                    await self.run_sys_call(content)
                    # Run The rest later
                    await section.pre_run(content, self.props, self.socket)
                    await section.run(content, self.props, self.socket)
                    await section.post_run(content, self.props, self.socket)
                except Exception as e:
                    if isinstance(e, SocketException):
                        try:
                            await self.action_handler(content, i, e)
                        except BreakLoop: break
                        except ContinueLoop: continue
                        except PassLoop: pass
                    else:
                        raise
                self.set_flag(i, True)
        # run_next_section = True
        # for i in range(len(self.sections)):
        #     section = self.sections[i]
        #     if not run_next_section:
        #         self.set_flag(i, True)
        #         run_next_section = True
        #         continue
        #     if not self.flags[i]:
        #         try:
        #             await section.pre_run(content, self.props, self.socket)
        #             await section.run(content, self.props, self.socket)
        #             await section.post_run(content, self.props, self.socket)
        #         except SectionError as e:
        #             await self.socket.send_json(
        #                 {'type' : 'err', 'msg' : e.message}
        #             )
        #             logging.error(e.message)
        #             await self.socket.close()
        #             break
        #         except WaitInput as e: break
        #         except SkipCurrent as e: continue
        #         except Disconnect as e: await self.socket.close()
        #         except SkipCurrentNoReturn:
        #             self.set_flag(i, True)
        #             continue
        #         except SkipNextNoReturn as e:
        #             run_next_section = False
        #             self.set_flag(i, True)
        #             continue
        #         self.set_flag(i, True)

    def set_flag(self, idx : int, value : bool):
        self.flags[idx] = value
    
    # Ran before any connection into the websocket
    async def pre_run(self):
        pass

    # Ran when connection is closed. 
    async def post_run(self):
        pass
