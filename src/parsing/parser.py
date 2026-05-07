from src.models.connection import Connection
from src.models.drone import Drone
from src.models.graph import Graph
from src.parsing.error_checker import ErrorChecker
import src.utils.exceptions as exc
from src.models.graph_keys import GraphKeys


class Parser:
    def __init__(self) -> None:
        self.graph: Graph = Graph()
        self.line_number: int = 0
        self.error_checker = ErrorChecker()

    def nb_drones_parser(self, drones_line: str, graph: Graph) -> None:

        # Split line, and remove ':'
        nb_drones, drone_count = drones_line.split()
        nb_drones = nb_drones.replace(":", "")

        # Error checker for nb_drone_parser
        self.error_checker.nb_drones_validator(
            self.line_number, nb_drones, drone_count, graph
        )

    def zone_parser(self, zone: str, graph: Graph) -> None:
        # Split line, and remove ":" from zone_ype
        main_data = zone.split("[")[0]
        zone_placeholder, zone_name, x, y = main_data.split()
        zone_placeholder = zone_placeholder.replace(":", "")

        # Error checker for zone_parser
        zone_obj = self.error_checker.zone_data_validator(x,
                                                          y,
                                                          zone_name,
                                                          zone)

        # Checking if zone is start, end or regualr
        zone_catagory: dict[str, str] = {
            "start_hub": "is_start",
            "end_hub": "is_end",
        }

        result = zone_catagory.get(zone_placeholder, "is_regular")
        setattr(zone_obj, result, True)

        graph.add_zone(zone_obj)

    def connection_parser(self, connection_line: str, graph: Graph) -> None:
        # Split line, take zone connections, remove ':'
        # If metadata is found, save it in a dictionary for later use
        # Create connection object
        try:
            zones = connection_line.split()[1]
        except IndexError as no_connection:
            print("Error: no connection found")
            raise no_connection
        zone_a, zone_b = zones.split("-")
        metadata = self.error_checker.connection_validator(connection_line)
        connection_obj = Connection(
            graph.get_zone(zone_a.strip()),
            graph.get_zone(zone_b.strip()),
            metadata.get(GraphKeys.MAX_LINK_CAPACITY, 1),
        )

        # Add connection object to graph
        graph.add_connection(connection_obj)

    def main_parser(self, file_path: str) -> None:
        with open(file_path, "r") as map_file:
            # Creating graph

            # Zone checks for parser
            zone_check = ["start_hub:", "end_hub:", "hub:"]
            try:
                for line in map_file:
                    stripped_line = line.strip()
                    # Skip if line is empthy or starts with '# '
                    if not stripped_line or stripped_line.startswith("#"):
                        continue
                    # Uses nb_drones_parser
                    elif "nb_drones:" in stripped_line:
                        self.nb_drones_parser(stripped_line, self.graph)
                    # Uses zone_parser if zone in zone_check
                    elif any(zone in stripped_line for zone in zone_check):
                        self.zone_parser(stripped_line, self.graph)
                    # Uses connection parser
                    elif "connection:" in stripped_line:
                        self.connection_parser(stripped_line, self.graph)
                    self.line_number += 1

                # Check if we have start zone to create
                # drones and set their start zone
                if self.graph.start_zone is None:
                    raise exc.ZoneNotFoundError("Start zone not found")
                if self.graph.start_zone.is_start:
                    start_zone = self.graph.start_zone
                    drone_count = self.graph.nb_drones_count
                    # Create a list of drones and add them to self.graph
                    for drone_id in range(1, (drone_count + 1)):
                        drone_obj = Drone(drone_id, start_zone)
                        self.graph.drones_list.append(drone_obj)
            except Exception as error:
                print(f"File line number: {self.line_number}")
                print(f"Error type: {type(error).__name__}")
                print(f"Error info: {error}")
                exit(1)
