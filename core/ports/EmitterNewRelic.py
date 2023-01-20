from core.domain.IEmitter import IEmitter

class EmitterNewRelic(IEmitter):
    
    def __init__(self, data: dict) -> None:
        self.data = data
    
    """
    Sumamry: Function to handle a configuration for the given emitter
    Parameters: A dictionary of configurations which are needed for initial setup
    Returns: None or just a silent return for a success status
    """
    def configure(self, data : dict) -> None:
        raise NotImplementedError    


    """
    Summary: Function to implement the process by which data is sent to a destination  
    Parameters: None
    Returns: None or just a status of success for each unit of measurement emitted
    """
    def trace_enable(self) -> None:
        raise NotImplementedError