

class ConnectionException(Exception):
    
    def __init__(self, message=None):
        if message is None:
            message = 'Bad connection with NWS'
        self.message = message
