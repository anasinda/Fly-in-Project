from src.models.graph import Graph
from src.models.zone import Zone
from src.models.drone import Drone
from src.models.connection import Connection
from src.utils.drone_in_transit import DroneInTransit
from src.utils.zone_types import ZoneType
from src.utils.exceptions import SimulationStuckError


class Simulator:
    """Simulator class that runs the drone routing simulation."""

    def __init__(self,
                 graph: Graph,
                 path: list[Zone],
                 drone_list: list[Drone]) -> None:
        """
        Initiliazing simulator class attributes
        """
        self.graph = graph
        self.path = path
        self.drone_list = drone_list
        self.turns: int = 0


    def drone_checker(self) -> None:
        """
        Remove arrived drones from active list and add to in_end
        """
        needs_removing: dict[str, Drone] = {}

        for drone in self.drone_list:
            if drone.has_arrived(self.graph.end_zone):
                needs_removing[drone.full_drone_id] = drone

        for key, value in needs_removing.items():
            self.graph.in_end[key] = value
            self.drone_list.remove(value)


    def run_simulation(self) -> int:
        """
        The simulator logic that sends drone in a way
        that makes them reach the end zone in the least
        possible turns and without conflicts
        """
        in_transit: dict[str, DroneInTransit] = {}
        try:
            while self.drone_list:

                # in-transit drones are drones that are going to
                # restricted zones, just arrived for drones that
                # are in restricted zone now, so we don't check them
                # later in the 2nd loop, turn_movements is for storing all
                # drone turns then printing them at once in one -line
                just_arrived: set[str] = set()
                turn_movements: list[str] = []
                for drone_id in list(in_transit.keys()):
                    # print("I'M HERE")
                    use_transit: DroneInTransit = in_transit[drone_id]
                    use_transit.turns_left -= 1
                    if use_transit.turns_left == 0:
                        # print("HERE HERE")
                        use_transit.transit_ender(turn_movements)
                        just_arrived.add(drone_id)
                        del in_transit[drone_id]

                for drone in self.drone_list:
                    # print("I'M HERE 2222 AND DRONE ID:", drone.full_drone_id)
                    if drone.full_drone_id in just_arrived:
                        # print("I'M HERE 3333")
                        continue
                    current_zone: Zone = drone.current_zone
                    # print(f"CURRENT ZONE {current_zone.zone_name} OF DRONE ID {drone.full_drone_id}")
                    next_zone: Zone = drone.next_zone_in_path()
                    # print(f"NEXT ZONE {next_zone.zone_name} OF DRONE ID {drone.full_drone_id}")
                    if next_zone is None:
                        # print("I'M HERE 4444")
                        continue
                    connections: list[Connection] = self.graph.get_zone_connections(current_zone.zone_name)
                    for connection in connections:
                        # print("CONNECTION LOOP")
                        # print("OTHER ZONE:", connection.other_zone(current_zone.zone_name))
                        if connection.other_zone(current_zone.zone_name) == next_zone:
                            # print("I'M HERE 5555")
                            # print("Max_link_cap: ", connection.check_link_usage())
                            # print("Zone cap: ", next_zone.can_accept_drone())
                            if connection.check_link_usage() and next_zone.can_accept_drone():
                                # print("I'M HERE 6666")
                                # check if zone is reserved or not because of restricted zones
                                if next_zone.check_if_reserved():
                                    # print("I'M HERE 7777")
                                    if next_zone.zone_type == ZoneType.RESTRICTED:
                                            # print("I'M HERE 8888")
                                            transit_obj = DroneInTransit(drone, connection, next_zone)
                                            transit_obj.transit_launcher(turn_movements)
                                            in_transit[drone.full_drone_id] = transit_obj
                                    else:
                                        # send drone normaly if zone is normal/priority
                                        # print("I'M HERE 9999")
                                        connection.drone_entry()
                                        drone.move_to(next_zone)
                                        connection.drone_exit()
                                        turn_movements.append(f"{drone}-{next_zone}")
                                        # print("This is drone ID:", drone.full_drone_id)
                        # break connection loop if drone moved to correct zone
                        # or zone is None because it's in-transit
                        if drone.current_zone != current_zone:
                            break
                        # print("In connection")
                # check if a drone has arrived to end so we can remove it
                # from drone_list, raise error if those two bellow are empthy
                # because if so, it means something happends that makes the
                # loop run infinitly
                self.drone_checker()
                if not turn_movements and not in_transit:
                    raise SimulationStuckError("All drones are blocked — possible deadlock")
                print(" ".join(turn_movements))
                self.turns += 1
        except SimulationStuckError as sim_e:
            print(f"[SIMULATION ERROR] {sim_e}")
            exit(1)
            # print("len of drone_list: ", self.drone_list)
        return self.turns





