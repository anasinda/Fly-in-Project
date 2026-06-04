from src.utils.zone_types import ZoneType
from src.utils.exceptions import BlockedZoneError


class Zone:
    """Represent a zone node with capacity, type, and metadata."""

    def __init__(
        self,
        x: int,
        y: int,
        zone_name: str,
        zone_type: ZoneType = ZoneType.NORMAL,
        zone_color: str | None = None,
        zone_capacity: int = 1
    ) -> None:
        """Initialize coordinates, identity, and zone settings."""

        self.x = x
        self.y = y
        self.zone_name = zone_name
        self.zone_type = zone_type
        self.zone_color = zone_color
        self.zone_capacity = zone_capacity
        self.current_drones: int = 0
        self.reservations: int = 0
        self.temp_cost: int | float = 0
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
        if self.is_start or self.is_end:
            return 1
        elif self.zone_type == ZoneType.RESTRICTED:
            return 2 + self.temp_cost
        elif self.zone_type == ZoneType.PRIORITY:
            return 0.5 + self.temp_cost
        elif self.zone_type == ZoneType.BLOCKED:
            raise BlockedZoneError("Cannot enter blocked zone:"
                                   f"{self.zone_name}")
        return 1 + self.temp_cost

    def increase_zone_cost(self) -> None:
        """Apply a small temporary cost to the zone."""
        self.temp_cost = 0.1

    def decrease_zone_cost(self) -> None:
        """Reset the temporary cost applied to the zone."""
        self.temp_cost = 0

    def check_if_reserved(self) -> bool:
        """Return whether the zone still has a free reservation slot."""
        if self.is_start or self.is_end:
            return True
        return (self.current_drones + self.reservations) < self.zone_capacity

    def check_if_restricted(self) -> bool:
        """Return whether the zone is restricted."""
        if self.zone_capacity == ZoneType.RESTRICTED:
            return True
        return False

    def __str__(self) -> str:
        """Return the zone name."""
        return f"{self.zone_name}"
