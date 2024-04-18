from abc import ABCMeta, abstractmethod


class IHarness(ABCMeta):
    
    """
    Summary: An interface to standardize the way emitters interact with the client code
    Parameters: An emitter class
    Returns: No returns expected
    
    """
    
    def __init__(self, emitter) -> None:
        raise NotImplementedError   
    
    
    @abstractmethod
    def configure(self, data: dict) -> None:
        """Function to change the configuration if needed for the service without restarting"""
        raise NotImplementedError   
    
    
    @abstractmethod
    def activate(self) -> None:
        """Expected to actually handle the wrapping of a class or function"""
        raise NotImplementedError   
    
    