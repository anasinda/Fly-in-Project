from src.models.graph import Graph
from src.models.zone import Zone
from src.models.drone import Drone
from src.models.connection import Connection


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
                connections: list[Connection] = self.graph.get_zone_connections(current_zone.zone_name)
                for connection in connections:
                    if connection.other_zone(current_zone.zone_name) == next_zone:
                        if connection.check_link_usage():
                            if next_zone.can_accept_drone():
                                connection.
                                drone.move_to(next_zone)




