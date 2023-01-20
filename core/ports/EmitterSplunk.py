from core.domain.IEmitter import IEmitter
import requests

"""
References: https://docs.splunk.com/Documentation/PythonSDK
"""

class EmitterSplunk(IEmitter):
    
    def __init__(self, data: dict) -> None:
        self.data = data
        
    """
    Sumamry: Function to handle a configuration for the given emitter
    Parameters: A dictionary of configurations which are needed for initial setup
    Returns: None or just a silent return for a success status
    """
    def configure(self, data : dict) -> None:
        self.hec_token = data['hec_token']    
        self.hec_endpoint = data['hec_endpoint']

    """
    Summary: Function to implement the process by which data is sent to a destination  
    Parameters: None
    Returns: None or just a status of success for each unit of measurement emitted
    """
    def trace_enable(self) -> None:
        self.log_message = "test message"
        
        response = requests.post(
            self.hec_endpoint,
            headers={"Authorization:" f"splunk {self.hec_token}"},
            data=self.log_message.encode()
        )
        
        if response.status_code == 200:
            print("Log detected. Starting process.")
            
        else:
            raise InterruptedError
    

def main():
    
    configuration = {
        "hec_token":"hf838d8whdwdwuh9u32f4f34f",
        "hec_endpoint":"https://example.com:8888/services/collector",
        }
    
    
    a = EmitterSplunk.configure(configuration)
    a.trace_enable()


if __name__ == '__main__':
    main()