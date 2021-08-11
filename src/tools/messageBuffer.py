

class MessageBuffer:
    """
    This class is used to store a message until it is sent to the server.
    """
    def __init__(self):
        self.messages = []

    def __str__(self) -> str:
        return ", ".join(str(self.messages))

    def add(self, message):
        """
        Adds a message to the buffer.
        """
        self.messages.append(message)

    def get(self):
        """
        get oldest message from buffer
        """
        if not self.messages: return None
        return self.messages.pop(0)

    def flush(self):
        """
        removes all messages from the buffer
        """
        self.messages = []

    def list(self):
        """
        returns a list of messages
        """
        return self.messages