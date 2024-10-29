class FactorySprites:
    def __init__(self, prototypes, periods, base_event_type):
        self._prototypes = prototypes
        self.periods = periods
        self.event_types = [base_event_type + i for i in range(len(prototypes))]
    def make(self, event_type):
        return self._prototypes[event_type - self.event_types[0]].clone()