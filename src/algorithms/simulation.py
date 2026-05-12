from src.models.graph import Graph
from src.models.zone import Zone
from src.models.drone import Drone


class Simulator:
    def __init__(self,
                 graph: Graph,
                 path: list[Zone],
                 drone_list: list[Drone]) -> None:
        self.graph = graph
        self.path = path
        self.drone_list = drone_list
        self.turns: int = 0
        self.drone_count = graph.nb_drones_count

    def run_simulation(self) -> None:

        while self.drone_count > 0:
            for drone in self.drone_list:
                current_zone: Zone = drone.current_zone
                next_zone: Zone = drone.next_zone_in_path()
                if 



