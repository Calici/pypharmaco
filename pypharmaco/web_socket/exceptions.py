import logging
from typing import \
    Union, \
    Literal
from abc import abstractmethod

class Action:
    BREAK = 'break'
    CONTINUE = 'continue'
    PASS = 'pass'

ActionT = Union[Literal['break'], Literal['continue'], Literal['pass']]

class BreakLoop(Exception):
    pass
class ContinueLoop(Exception):
    pass
class PassLoop(Exception):
    pass

class SocketException(Exception):
    @abstractmethod
    def action(self):
        raise NotImplementedError
    def throw_exec(self):
        if self.action() == 'break':
            raise BreakLoop
        elif self.action() == 'pass':
            raise PassLoop
        elif self.action() == 'continue':
            raise ContinueLoop

# An SocketException exit with an error
class SectionError(SocketException):
    """
        Throws a Section Error that disconnects the socket
    """
    def __init__(self, message : str):
        self.message    = message
    def __repr__(self):
        return self.message
    def action(self):
        return Action.BREAK
    
# An SocketException issued to wait for the next input
class WaitInput(SocketException):
    """
        Waits for a new input to arrive
    """
    def action(self):
        return Action.BREAK

# An SocketException to WaitInput before executing the next one
class WaitInputForNext(SocketException):
    """
        Waits for a new input to arrive for the next one.
    """
    def action(self):
        return Action.BREAK

# An SocketException issued to skip the current section to the next section [Does not change the boolean flag]
class SkipCurrent(SocketException):
    """
        Skips the current section to the next section
    """
    __slots__ = ('return_to_section', )
    def __init__(self, return_to_section : bool = True):
        self.return_to_Section = return_to_section
    def action(self):
        return Action.CONTINUE

# An SocketException to skip the current section and Set boolean Flag
class SkipCurrentNoReturn(SocketException):
    def __init__(self):
        logging.warning("DEPRECATED: use SkipCurrent with an argument")
    def action(self):
        return Action.CONTINUE

# An SocketException to skip the next section [Changes the boolean flag]
class SkipNextNoReturn(SocketException):
    def action(self):
        return Action.CONTINUE

# An SocketException to disconnect
class Disconnect(SocketException):
    def action(self):
        return Action.BREAK

# Jump to Previous Sections
class JumpSection(SocketException):
    """
        Jumps to previous section, if backwards, undos all the flags that have 
        already been set, if forward, sets the flag
    """
    __slots__ = ('target', )
    def __init__(self, target : int):
        self.target = target
    def action(self):
        return Action.BREAK
