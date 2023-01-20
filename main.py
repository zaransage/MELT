from MELT.core.adaptors.MELTClient import MELTClient
from MELT.core.ports.EmitterNewRelic import EmitterNewRelic


class PretendProgram():
    def __init__(self, number_first : int, number_second : int) -> int:
        self.number_first = number_first
        self.number_second = number_second
        
    def calculate(self):
        return self.number_first * self.number_second
    
      
def main():
        
    results = PretendProgram(5,7)
    print(results.calculate())
    

if __name__ == '__main__':
    melt_engine = MELTClient(EmitterNewRelic())
    melt_engine.activate()
    main()