class BlockedZoneError(Exception):
    """Raised when a drone attempts to enter a blocked zone."""
    pass


class ZoneNotFoundError(Exception):
    """
    Raised when trying to retrieve a zone
    that doesn't exist in connection
    """
    pass


class DuplicateZoneError(Exception):
    """
    Raised when finding a zone
    in our zones dictionary with the same name
    """
    pass


class DuplicateConnectionError(Exception):
    """
    Raised when finding a duplicate connection
    when parsing file
    """
    pass
