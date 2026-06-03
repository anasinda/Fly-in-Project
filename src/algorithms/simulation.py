from src.models.graph import Graph
from src.models.zone import Zone
from src.models.drone import Drone
from src.models.connection import Connection
from src.utils.drone_in_transit import DroneInTransit
from src.utils.zone_types import ZoneType
from src.utils.exceptions import SimulationStuckError, ZoneNotFoundError


class Simulator:
    """Simulator class that runs the drone routing simulation."""

    def __init__(self,
                 graph: Graph,
                 drone_list: list[Drone]) -> None:
        """
        Initiliazing simulator class attributes
        """
        self.graph = graph
        self.drone_list = drone_list
        self.turns: int = 0

    def drone_checker(self) -> None:
        """
        Remove arrived drones from active list and add to in_end
        """
        needs_removing: dict[str, Drone] = {}

        for drone in self.drone_list:
            if self.graph.end_zone and drone.has_arrived(self.graph.end_zone):
                needs_removing[drone.full_drone_id] = drone

        for key, value in needs_removing.items():
            self.graph.in_end[key] = value
            self.drone_list.remove(value)

    def check_in_transit(self, turn_movements: list[str], in_transit: dict[str, DroneInTransit]) -> set[str]:
        just_arrived: set[str] = set()
        for drone_id in list(in_transit.keys()):
            use_transit: DroneInTransit = in_transit[drone_id]
            use_transit.turns_left -= 1
            if use_transit.turns_left == 0:
                use_transit.transit_ender(turn_movements)
                just_arrived.add(drone_id)
                del in_transit[drone_id]
        return just_arrived

    def connection_finder(self, current_zone: Zone, next_zone:Zone,
                          drone: Drone, turn_movements: list[str],
                          in_transit: dict[str, DroneInTransit],
                          used_connections: list[Connection],
                          connections: list[Connection]):

        for connection in connections:
            other_zone: Zone = connection.other_zone(current_zone.zone_name)
            link_check: bool = connection.check_link_usage()
            drone_cap_check: bool = next_zone.can_accept_drone()
            reserved_check: bool = next_zone.check_if_reserved()
            restricted_check : ZoneType = next_zone.zone_type

            if other_zone == next_zone:
                if link_check and drone_cap_check:
                    if reserved_check:
                        if restricted_check == ZoneType.RESTRICTED:
                            transit_obj = DroneInTransit(drone, connection, next_zone)
                            transit_obj.transit_launcher(turn_movements)
                            drone_id: str = drone.full_drone_id
                            in_transit[drone_id] = transit_obj
                        else:
                            connection.drone_entry()
                            used_connections.append(connection)
                            drone.move_to(next_zone)
                            turn_movements.append(f"{drone}-{next_zone}")
            if drone.current_zone != current_zone:
                break


    def drone_sender(self, just_arrived: set[str], turn_movements: list[str],
                     in_transit: dict[str, DroneInTransit], used_connections: list[Connection]):
        for drone in self.drone_list:
            if drone.full_drone_id in just_arrived:
                continue
            current_zone: Zone | None = drone.current_zone
            next_zone: Zone | None = drone.next_zone_in_path()
            if next_zone is None or current_zone is None:
                continue
            connections: list[Connection] = []
            connections = self.graph.get_zone_connections(current_zone.zone_name)
            self.connection_finder(current_zone, next_zone, drone, turn_movements, in_transit, used_connections, connections)

    def run_simulation(self) -> tuple[int, list[list[str]]]:
        """
        The simulator logic that sends drone in a way
        that makes them reach the end zone in the least
        possible turns and without conflicts
        """
        in_transit: dict[str, DroneInTransit] = {}
        simulation_log: list[list[str]] = []
        try:
            while self.drone_list:
                # in-transit drones are drones that are going to
                # restricted zones, just arrived for drones that
                # are in restricted zone now, so we don't check them
                # later in the 2nd loop, turn_movements is for storing all
                # drone turns then printing them at once in one -line

                turn_movements: list[str] = []
                just_arrived = self.check_in_transit(turn_movements, in_transit)
                used_connections: list[Connection] = []
                self.drone_sender(just_arrived, turn_movements, in_transit, used_connections)
                self.drone_checker()
                if not turn_movements and not in_transit:
                    raise SimulationStuckError(
                        "All drones are blocked — possible deadlock"
                    )
                for used_connection in used_connections:
                    used_connection.drone_exit()
                simulation_log.append(turn_movements)
                print(" ".join(turn_movements))
                self.turns += 1
        except (SimulationStuckError, ZoneNotFoundError) as sim_e:
            print(f"[SIMULATION ERROR] {sim_e}")
            exit(1)
            # print("len of drone_list: ", self.drone_list)
        return self.turns, simulation_log
