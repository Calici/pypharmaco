import logging
# An exception exit with an error
class SectionError(Exception):
    def __init__(self, message : str):
        self.message    = message
    def __repr__(self):
        return self.message
    
# An exception issued to wait for the next input
class WaitInput(Exception):
    pass

# An Exception to WaitInput before executing the next one
class WaitInputForNext(Exception):
    pass

# An exception issued to skip the current section to the next section [Does not change the boolean flag]
class SkipCurrent(Exception):
    __slots__ = ('return_to_section', )
    def __init__(self, return_to_section : bool = True):
        self.return_to_Section = return_to_section
    pass

# An exception to skip the current section and Set boolean Flag
class SkipCurrentNoReturn(Exception):
    def __init__(self):
        logging.warning("DEPRECATED: use SkipCurrent with an argument")

# An exception to skip the next section [Changes the boolean flag]
class SkipNextNoReturn(Exception):
    pass

# An exception to disconnect
class Disconnect(Exception):
    pass

# Jump to Previous Sections
class JumpSection(Exception):
    """
        Jumps to previous section, if backwards, undos all the flags that have 
        already been set, if forward, sets the flag
    """
    __slots__ = ('target', )
    def __init__(self, target : int):
        self.target = target