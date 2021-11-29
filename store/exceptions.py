class ResourceNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super(ResourceNotFoundException, self).__init__(message)


class InvalidParameterException(Exception):
    def __init__(self, message):
        self.message = message
        super(InvalidParameterException, self).__init__(message)


class ServerException(Exception):
    def __init__(self, message):
        self.message = message
        super(ServerException, self).__init__(message)
