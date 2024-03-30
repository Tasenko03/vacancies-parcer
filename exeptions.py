class IncorrectSeedURLError(TypeError):
    """
    seed URL does not match standard pattern
    """


#class NumberOfArticlesOutOfRangeError(Exception):
#    """
#    total number of articles is out of range from 1 to 150
#    """


#class IncorrectNumberOfArticlesError(Exception):
#    """
#    total number of articles to parse is not integer
#    """


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

