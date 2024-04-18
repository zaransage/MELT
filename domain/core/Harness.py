from core.domain.IHarness import IHarness

class Harness(IHarness):
    def __init__(self, emitter) -> None:
        self.emitter = emitter
    
    def configure(self, configuration : dict) -> None:
        self.emitter.configure(configuration)
    
    def activate(self) -> None:
        self.emitter.trace_enable()