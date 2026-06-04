from src.models.drone import Drone
from src.models.connection import Connection
from src.models.zone import Zone


class DroneInTransit:
    """Track a drone while it is moving through a connection."""

    def __init__(self, drone: Drone, connection: Connection,
                 next_zone: Zone) -> None:
        """Store the drone, connection, and destination zone."""
        self.drone = drone
        self.connection = connection
        self.next_zone = next_zone
        self.turns_left: int = 1

    def transit_launcher(self, turn_movements: list[str]) -> None:
        """Start the transit and log the movement."""
        self.connection.drone_entry()
        self.next_zone.reservations += 1
        if self.drone.current_zone is not None:
            self.drone.current_zone.current_drones -= 1
        self.drone.remove_current_zone()
        turn_movements.append(f"{self.drone}-{self.connection}")

    def transit_ender(self, turn_movements: list[str]) -> None:
        """Finish the transit and log the arrival."""
        self.connection.drone_exit()
        self.next_zone.reservations -= 1
        self.drone.move_to(self.next_zone)
        turn_movements.append(f"{self.drone}-{self.drone.current_zone}")
