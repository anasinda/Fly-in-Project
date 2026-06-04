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


class SameMetadataError(Exception):
    """
    Raised when finding same metadata when
    parsing file
    """

    pass


class NoPathFoundError(Exception):
    """
    Raised when not checking if end in dist_list
    if still infinity
    """

    pass


class SimulationStuckError(Exception):
    """
    Raised when there is a problem in the simulation
    that let's it run infinitly
    """

    pass


class ParserError(Exception):
    """
    Raised when finding an error during file parsing
    """

    pass


class MetadataError(Exception):
    """
    Raised when finding the wrong type of metadata
    """

    pass


class ConnectionError(Exception):
    """
    Raised when not finding a zone from connection
    in zones list in graph
    """

    pass


class EmptyFileException(Exception):
    """
    Raised when opening an empthy file
    """

    pass


class DuplicateCoordinates(Exception):
    """
    Raised when findinng duplicate x or y coordinates
    """

    pass
