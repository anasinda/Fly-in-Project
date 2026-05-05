from models.zone_types import ZoneType
from utils.exceptions import BlockedZoneError


class Zone:
    """Class that generates a zone object for our graph"""

    def __init__(
        self,
        x: int,
        y: int,
        zone_name: str,
        zone_type: str = ZoneType.NORMAL.value,
        zone_color: str | None = None,
        zone_capacity: int = 1,
    ):

        self.x = x
        self.y = y
        self.zone_name = zone_name
        self.zone_type = zone_type
        self.zone_color = zone_color
        self.zone_capacity = zone_capacity
        self.current_drones = 0
        self.is_start = False
        self.is_end = False
        self.is_regular = False

    def can_accept_drone(self) -> bool:
        """Check if the zone has capacity for an additional drone."""
        return self.current_drones < self.zone_capacity

    def zone_move_cost(self) -> int:
        """Check zone cost or if it is blocked."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        elif self.zone_type == ZoneType.BLOCKED:
            raise BlockedZoneError("Cannot enter blocked zone:"
                                   f"{self.zone_name}")
        else:
            return 1
