from src.models.zone import Zone
from src.utils.exceptions import ZoneNotFoundError


class Connection:
    """Represent a link between two zones."""

    def __init__(self,
                 zone_a: Zone,
                 zone_b: Zone,
                 max_link_capacity: int = 1) -> None:
        """Initialize both endpoints and the link capacity."""
        self.max_link_capacity = max_link_capacity
        self.current_usage: int = 0
        self.zone_b: Zone = zone_b
        self.zone_a: Zone = zone_a

    def check_link_usage(self) -> bool:
        """Return whether the connection can accept another drone."""
        return self.current_usage < self.max_link_capacity

    def other_zone(self, zone_get: str) -> Zone:
        """Return the opposite endpoint for a given zone name."""
        zone_getter = {
            self.zone_a.zone_name: self.zone_b,
            self.zone_b.zone_name: self.zone_a,
        }
        if zone_get not in zone_getter:
            raise ZoneNotFoundError(
                f"Zone '{zone_get}'" f"is not part of this connection: {self}"
            )
        return zone_getter[zone_get]

    def drone_entry(self) -> None:
        """Mark a drone as entering the connection."""
        self.current_usage += 1

    def drone_exit(self) -> None:
        """Mark a drone as leaving the connection."""
        self.current_usage -= 1

    def __str__(self) -> str:
        """Return the connection endpoints as a readable string."""
        return f"{self.zone_a.zone_name}-{self.zone_b.zone_name}"
