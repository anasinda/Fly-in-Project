from src.models.drone import Drone
from src.models.connection import Connection
from src.models.zone import Zone


class DroneInTransit:
    def __init__(self,
                 drone: Drone,
                 connection: Connection,
                 next_zone: Zone):
        self.drone = drone
        self.connection = connection
        self.next_zone = next_zone
        self.turns_left: int = 1

    def transit_launcher(self, turn_movements: list[str]):
        self.connection.drone_entry()
        self.next_zone.reservations += 1
        self.drone.remove_current_zone()
        turn_movements.append(f"{self.drone}-{self.connection}")

    def transit_ender(self, turn_movements: list[str]):
        self.connection.drone_exit()
        self.drone.move_to(self.next_zone)
        turn_movements.append(f"{self.drone-self.drone.current_zone}")





