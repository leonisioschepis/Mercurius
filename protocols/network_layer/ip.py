from entities.scenario import Scenario

class ip:
    def __init__(self):
        self.header = Scenario().getattr('config')['ip']['standard_header']

    def get_cost(self, pdu):
        return self.header + pdu
