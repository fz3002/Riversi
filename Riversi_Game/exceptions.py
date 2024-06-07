class FieldTakenException(Exception):
    """Exception raised when trying to chose taken field"""
    def __init__(self, message):
        super().__init__(message)
