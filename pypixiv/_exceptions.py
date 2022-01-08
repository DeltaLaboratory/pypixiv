class ArtworkNotFound(Exception):
    """
    raised when artwork not found
    """
    pass


class InternalError(Exception):
    """
    raised when internal error(unexpected response, or whatever we didn't expect)
    please report this exception at https://github.com/DeltaLaboratory/pypixiv/issues
    if you found this exception with error message
    """
    pass
