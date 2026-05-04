class BlockedZoneError(BaseException):
    """Raised when a drone attempts to enter a blocked zone."""
    pass


class ZoneNotFoundError(BaseException):
    """
    Raised when trying to retrieve a zone
    that doesn't exist in connection
    """
    pass


class DuplicateZoneError(BaseException):
    """
    Raised when finding a zone
    in our zones dictionary with the same name
    """
    pass


class DuplicateConnectionError(BaseException):
    """
    Raised when finding a duplicate connection
    when parsing file
    """
    pass


class DuplicateDroneCountLineError(BaseException):
    """
    Raised when finding a duplicate drone count
    line when parsing file
    """
    pass


class DuplicateStartOrEndZoneError(BaseException):
    """
    Raised when finding a duplicate start or end zone
    when parsing file
    """
    pass


class ZoneTypeError(Exception):
    """
    Raised when finding a wrong zone_type during
    parsing
    """
    pass

class GraphKeyError(Exception):
    """
    Raised when finding a metadata that is not
    supported during parsing
    """
