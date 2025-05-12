from timedependentparty.TimeDependentParty import TimeDependentParty
from tudelft_utilities_logging.Reporter import Reporter

class Linear (TimeDependentParty):
    """
    A simple party that places random bids and accepts when it receives an offer
    with sufficient utility.    
    """
    def __init__(self, reporter: Reporter=None):
        super().__init__(reporter)

    #Override
    def getDescription(self) -> str:
        return "Linear: concedes linearly with time. "\
                + "Parameters minPower (default 1) and maxPower (default infinity) are used when voting"
    #Override
    def getE(self)->float:
        return 1.0
