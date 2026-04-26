class BlockedZoneError(Exception):
    """Raised when a drone attempts to enter a blocked zone."""
    pass


class ZoneNotFoundError(Exception):
    """
    Raised when trying to retrieve a zone
    that doesn't exist in connection
    """
    pass
