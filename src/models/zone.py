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
        zone_capacity: int = 1
    ):

        self.x = x
        self.y = y
        self.zone_name = zone_name
        self.zone_type = zone_type
        self.zone_color = zone_color
        self.zone_capacity = zone_capacity
        self.current_drones: int = 0
        self.reservations: int = 0
        self.temp_cost: int = 0
        self.is_start: bool = False
        self.is_end: bool = False
        self.is_regular: bool = False

    def can_accept_drone(self) -> bool:
        """Check if the zone has capacity for an additional drone."""
        if self.is_start or self.is_end:
            return True
        return self.current_drones < self.zone_capacity

    def zone_move_cost(self) -> float:
        """Check zone cost or if it is blocked."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2 + self.temp_cost
        elif self.zone_type ==  ZoneType.PRIORITY:
            return 0.5 + self.temp_cost
        elif self.zone_type == ZoneType.BLOCKED:
            raise BlockedZoneError("Cannot enter blocked zone:"
                                   f"{self.zone_name}")
        else:
            if self.is_start or self.is_end:
                return 1
            return 1 + self.temp_cost

    def increase_zone_cost(self) -> None:
        self.temp_cost += 100

    def decrease_zone_cost(self) -> None:
        self.temp_cost -= 100

    def check_if_reserved(self) -> bool:
        if self.is_start or self.is_end:
            return True
        return (self.current_drones + self.reservations) < self.zone_capacity

    def __str__(self):
        return f"{self.zone_name}"
