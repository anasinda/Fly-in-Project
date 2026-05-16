from src.models.drone import Drone
from src.models.zone import Zone


class DronePathSetter:
    """
    A class that sets the path that each drone takes
    """

    def __init__(self, paths: dict[str, list[Zone]], drone_list: list[Drone]) -> None:
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
        if self.paths['best_path'] and self.paths['longer_path'] is None:
            for drone in self.drone_list:
                drone.path = self.paths['best_path']
        else:
            total_cost: int = self.paths['first_path'] + self.paths['second_path']
            lowest_bottleneck: int = min((self.paths['first_path'], self.paths['second_path']))
            for index, drone in enumerate(self.drone_list):
                if index % total_cost < lowest_bottleneck:
                    drone.path = self.paths['longer_path']
                else:
                    drone.path = self.paths['best_path']
