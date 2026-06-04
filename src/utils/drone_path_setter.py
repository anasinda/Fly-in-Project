from src.models.drone import Drone
from src.models.zone import Zone


class DronePathSetter:
    """Assign a discovered path to each drone."""

    def __init__(self, paths: list[list[Zone]],
                 drone_list: list[Drone]) -> None:
        """Store the available paths and drones to configure."""
        self.paths = paths
        self.drone_list = drone_list

    def set_drones_path(self) -> None:
        """Assign paths to drones in a round-robin fashion."""
        for index, drone in enumerate(self.drone_list):
            path_index = index % len(self.paths)
            drone.path = self.paths[path_index]
