class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.state = None

    def addState(self, name, handler):
        name = name.upper()
        self.handlers[name] = handler

    def setStart(self, name):
        self.state = name.upper()

    def step(self):
        try:
            handler = self.handlers[self.state.upper()]
        except:
            raise InitializationError("must call .set_start() before .run()")
        
        (self.state,image) = handler()

        return image
