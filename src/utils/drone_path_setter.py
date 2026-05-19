from src.models.drone import Drone
from src.models.zone import Zone


class DronePathSetter:
    """
    A class that sets the path that each drone takes
    """

    def __init__(self, paths: list[list[Zone]], drone_list: list[Drone]) -> None:
        """
        Initiliazing class attributes for use
        """
        self.paths = paths
        self.drone_list = drone_list

    def set_drones_path(self) -> None:
        """
        Loops over the drone list and sets path found
        from pathfinding algo for each one
        """
        for index, drone in enumerate(self.drone_list):
            path_index = index % len(self.paths)
            drone.path = self.paths[path_index]
