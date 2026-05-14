from src.models.graph import Graph
from src.models.zone import Zone
from src.models.drone import Drone
from src.models.connection import Connection
from src.utils.drone_in_transit import DroneInTransit
from src.models.zone_types import ZoneType


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


    def run_simulation(self) -> int:

        turns: int = 0
        in_transit: dict[str, DroneInTransit] = {}
        while self.drone_count > 0:

            just_arrived = set()
            turn_movements: list[str] = []
            for drone_id in list(in_transit.keys()):
                use_transit: DroneInTransit = in_transit[drone_id]
                use_transit.turns_left -= 1
                if use_transit.turns_left == 0:
                    use_transit.transit_ender(turn_movements)
                    just_arrived.add(drone_id)
                    del in_transit[drone_id]

            for drone in self.drone_list:
                if drone.full_drone_id in just_arrived:
                    continue
                current_zone: Zone = drone.current_zone
                next_zone: Zone = drone.next_zone_in_path()
                connections: list[Connection] = self.graph.get_zone_connections(current_zone.zone_name)
                for connection in connections:
                    if connection.other_zone(current_zone.zone_name) == next_zone:
                        if connection.check_link_usage() and next_zone.can_accept_drone():
                            if next_zone.check_if_reserved():
                                if next_zone.zone_type == ZoneType.RESTRICTED.value:
                                        transit_obj = DroneInTransit(drone, connection, next_zone)
                                        transit_obj.transit_launcher(turn_movements)
                                        in_transit[drone.full_drone_id] = transit_obj
                                else:
                                    connection.drone_entry()
                                    drone.move_to(next_zone)
                                    connection.drone_exit()
                                    turn_movements.append(f"{drone}-{next_zone}")
                    if drone.current_zone != current_zone:
                        break
            if drone.has_arrived(self.graph.end_zone):
                self.drone_count -= 1
            print(" ".join(turn_movements))
            turns += 1
        return turns





