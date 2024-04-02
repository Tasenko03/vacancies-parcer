class IncorrectSeedURLError(TypeError):
    """
    seed URL does not match standard pattern
    """

class IncorrectHeadersError(Exception):
    """
    headers are not in a form of dictionary
    """


class IncorrectEncodingError(Exception):
    """
    encoding must be specified as a string
    """


class IncorrectTimeoutError(Exception):
    """
    timeout value must be a positive integer less than 60
    """


class IncorrectVerifyError(Exception):
    """
     verify certificate value must either be True or False
     """

