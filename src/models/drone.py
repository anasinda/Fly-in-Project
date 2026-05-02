from models.zone import Zone


class Drone:
    """Class that creates drone object"""
    def __init__(self, drone_id: int, current_zone: Zone) -> None:
        self.drone_id: int = drone_id
        self.full_drone_id: str = "D" + str(drone_id)
        self.current_zone: Zone = current_zone
        self.path: list[Zone] = []

    def move_to(self, zone: Zone) -> None:
        """Moves drone from one zone to the next"""
        self.current_zone.current_drones -= 1
        self.current_zone = zone
        self.current_zone.current_drones += 1

    def has_arrived(self, end_zone: Zone) -> bool:
        """Checks if drone reached goal/end_zone"""
        return self.current_zone == end_zone

    def __str__(self) -> str:
        """Prints drone id"""
        return f"D{self.drone_id}"
