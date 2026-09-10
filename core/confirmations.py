class ConfirmationManager:
    def __init__(self):
        self.pending = None

    def set(self, action):
        self.pending = action

    def pop(self):
        action = self.pending
        self.pending = None
        return action

    def has_pending(self):
        return self.pending is not None
