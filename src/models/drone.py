from src.models.zone import Zone


class Drone:
    """Class that creates drone object"""

    def __init__(self, drone_id: int, current_zone: Zone) -> None:
        self.drone_id: int = drone_id
        self.full_drone_id: str = "D" + str(drone_id)
        self.current_zone: Zone | None = current_zone
        self.path: list[Zone] = []
        self.path_index: int = 0

    def move_to(self, zone: Zone) -> None:
        """Moves drone from one zone to the next"""
        self.current_zone.current_drones -= 1
        self.current_zone = zone
        self.current_zone.current_drones += 1

    def remove_current_zone(self) -> None:
        self.current_zone = None

    def has_arrived(self, end_zone: Zone) -> bool:
        """Checks if drone reached goal/end_zone"""
        return self.current_zone == end_zone

    def next_zone_in_path(self) -> Zone | None:
        """
        Returns the next zone in the path, or None if at end of path.
        """
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def __str__(self) -> str:
        """Prints drone id"""
        return f"D{self.drone_id}"
