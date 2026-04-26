from models.zone import Zone
from utils.exceptions import ZoneNotFoundError


class Connection:
    """Class that creates a connection object for our graph"""
    def __init__(self,
                 zone_a: Zone,
                 zone_b: Zone,
                 max_link_capacity: int = 1) -> None:
        self.max_link_capacity = max_link_capacity
        self.current_usage: int = 0
        self.zone_b: Zone = zone_b
        self.zone_a: Zone = zone_a

    def can_accept_drone(self) -> bool:
        """Check if connection has capacity to add drones to the link"""
        return self.current_usage < self.max_link_capacity

    def has_zone(self, zone_check: str) -> bool:
        """Check if sent zone is inside this connection"""
        return zone_check in {self.zone_a.zone_name, self.zone_b.zone_name}

    def other_zone(self, zone_get: str) -> Zone:
        """Grab other corresponding zone"""
        zone_getter = {
            self.zone_a.zone_name: self.zone_b,
            self.zone_b.zone_name: self.zone_a
        }
        if zone_get not in zone_getter:
            raise ZoneNotFoundError(f"Zone '{zone_get}'"
                                    f"is not part of this connection: {self}")
        return zone_getter[zone_get]

    def drone_entry(self) -> None:
        """Increment connection usage"""
        self.current_usage += 1

    def drone_exit(self) -> None:
        """Decrement connection usage"""
        self.current_usage -= 1

    def check_current_usage(self) -> int:
        """Check current connection usage"""
        return self.current_usage

    def __str__(self) -> str:
        """Print zone names inside connection"""
        return f"{self.zone_a.zone_name}-{self.zone_b.zone_name}"
