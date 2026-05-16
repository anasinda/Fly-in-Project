from src.models.graph import Graph
from src.models.drone import Drone
from src.models.zone import Zone


class DronePathSetter:
    """
    A class that sets the path that each drone takes
    """
    def __init__(self,
                 path: list[Zone],
                 drone_list: list[Drone]) -> None:
        """
        Initiliazing class attributes for use
        """
        self.path = path
        self.drone_list = drone_list

    def set_drones_path(self) -> None:
        """
        Loops over the drone list and sets path found
        from pathfinding algo for each one
        """
        for drone in self.drone_list:
            drone.path = self.path.copy()
