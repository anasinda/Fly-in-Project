from src.utils.zone_types import ZoneType
from src.utils.exceptions import BlockedZoneError


class Zone:
    """Class that generates a zone object for our graph"""

    def __init__(
        self,
        x: int,
        y: int,
        zone_name: str,
        zone_type: ZoneType = ZoneType.NORMAL,
        zone_color: str | None = None,
        zone_capacity: int = 1,
    ):

        self.x = x
        self.y = y
        self.zone_name = zone_name
        self.zone_type = zone_type
        self.zone_color = zone_color
        self.zone_capacity = zone_capacity
        self.current_drones: int = 0
        self.reservations: int = 0
        self.is_start: bool = False
        self.is_end: bool = False
        self.is_regular: bool = False

    def can_accept_drone(self) -> bool:
        """Check if the zone has capacity for an additional drone."""
        if self.is_start or self.is_end:
            return True
        return self.current_drones < self.zone_capacity

    def zone_move_cost(self) -> int:
        """Check zone cost or if it is blocked."""
        if self.zone_type == ZoneType.RESTRICTED.value:
            return 2
        elif self.zone_type == ZoneType.BLOCKED.value:
            raise BlockedZoneError("Cannot enter blocked zone:"
                                   f"{self.zone_name}")
        else:
            return 1

    def check_if_reserved(self) -> bool:
        if self.is_start or self.is_end:
            return True
        return (self.current_drones + self.reservations) < self.zone_capacity

    def __str__(self):
        return f"{self.zone_name}"
