'''
The simulation scenario is a Singleton, and parameters can be set up only once.
Singleton principles: https://refactoring.guru/design-patterns/Scenario
'''
import logging

class Scenario:
    class __Scenario:
        def __init__(self):
            self.num_devices = None
            self.application_layer = None
            self.transport_layer = None
            self.network_layer = None
            self.link_layer = None
            self.config = None
            self.cell = None

        def __str__(self):
            return 'Stack: %s | %s | %s | %s' %(self.application_layer, self.transport_layer, self.network_layer, self.link_layer)

    instance = None

    def __init__(self):
        if not Scenario.instance:
            Scenario.instance = Scenario.__Scenario()

    def getattr(self, name):
        return getattr(self.instance, name)

    def setattr(self, name, value):
        if not getattr(self.instance, name):
            setattr(self.instance, name, value)
        else:
            logging.warn('%s parameter already set up, ignored statement' %(name))

    def __str__(self):
        return str(self.instance)
