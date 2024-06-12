"""Exceptions module"""


class FieldTakenException(Exception):
    """Exception raised when trying to chose taken field"""

    def __init__(self, message):
        super().__init__(message)


class SaveFormatException(Exception):
    """Exception raised when save format is wrong or corrupt

    Args:
        Exception (Exception): Extends
    """

    def __init__(self, message):
        super().__init__(message)
