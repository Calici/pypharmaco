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
    pass

# An exception to skip the current section and Set boolean Flag
class SkipCurrentNoReturn(Exception):
    pass

# An exception to skip the next section [Changes the boolean flag]
class SkipNextNoReturn(Exception):
    pass

# An exception to disconnect
class Disconnect(Exception):
    pass
