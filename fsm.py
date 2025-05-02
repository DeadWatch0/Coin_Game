class StateMachine:
    def __init__(self, initial):
        self.current = initial
        self._handlers = {}

    def add(self, state, handler):
        self._handlers[state] = handler

    def transition(self, new_state):
        self.current = new_state

    def run(self):
        handler = self._handlers.get(self.current)
        if handler:
            return handler()
        else:
            raise ValueError(f"No handler for state {self.current}")
