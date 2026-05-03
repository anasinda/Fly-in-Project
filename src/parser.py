from models.connection import Connection
from models.drone import Drone
from models.graph import Graph
from models.zone_types import ZoneType
from models.zone import Zone
from models.error_checker import ErrorChecker
import utils.exceptions as exc
from typing import Any


class Parser:
    def __init__(self):
        self.graph: Graph = Graph()
        self.line_number: int = 0
        self.error_checker = ErrorChecker()

    def nb_drones_parser(self, drones_line: str, graph: Graph) -> None:

        # Split line, and remove ':'
        nb_drones, drone_count = drones_line.split()
        nb_drones = nb_drones.replace(":", "")

        # Error checker for nb_drone_parser
        self.error_checker.nb_drones_error_checker(nb_drones,
                                                   drone_count,
                                                   graph.nb_drones_check,
                                                   graph.nb_drones_count)
        print("sadadsadaddsadsadsadsa")

    def zone_parser(self, zone: str, graph: Graph) -> None:
        # Split line, and remove ":" from zone_ype
        main_data = zone.split("[")[0]
        zone_placeholder, zone_name, x, y = main_data.split()
        zone_placeholder = zone_placeholder.replace(":", "")


        # Check if x and y are digits
        if not x.isdigit() or not y.isdigit():
            raise ValueError(f"{x} or {y} is not  number")


        # Turn x and y charachter values to integer values
        x, y = map(int, [x, y])

        # Check if x and y are negative
        if x < 0 or y < 0:
            raise ValueError(f"x position: {x}"
                             f"or y position: {y} not acceptable")

        # Split metadata and save it in a dictionary
        metadata = dict()
        if "[" in zone:
            extradata = zone.split("[")[-1].replace("]", "")
            for data in extradata.split():
                key, value = data.split("=")
                metadata[key] = value

            # Store metadata and set default values if not found
            zone_color: str = metadata.get("color", None)
            zone_capacity: str | Any = metadata.get("max_drones", "1")

            # Check if zone_capacity is a number
            if not zone_capacity.isdigit():
                raise ValueError("zone capacity:"
                                     f"{zone_capacity} is not a number")

            # Change zone capacity from an str to an int
            zone_capacity = int(zone_capacity)

            # Remove whitespaces from names
            zone_placeholder = zone_placeholder.strip()
            zone_name = zone_name.strip()

            # Check zone_type exists
            try:
                zone_type = ZoneType(metadata.get("zone", "normal"))
            except ValueError as type_error:
                raise type_error(f"line number: {self.line_number}\n"
                                 "Invalid zone type:"
                                 f"'{metadata["zone"]}'\n{type_error}")

            # Creating zone object
            zone_obj = Zone(x, y,
                            zone_name,
                            zone_type,
                            zone_color,
                            zone_capacity)

            # Checking if zone is start or end
            if zone_placeholder == "start_hub":
                zone_obj.is_start = True
            elif zone_placeholder == "end_hub":
                zone_obj.is_end = True
            else:
                zone_obj.is_regular = True

            # Adding zone to zones dictionray in our graph
            graph.add_zone(zone_obj)

    def connection_parser(self,
                          connection_line: str,
                          graph: Graph) -> None:
        # Split line, only take two parts, remove ':', split zone connections
        zones = connection_line.split()[1]

        #  connection.replace(":", "")
        zone_a, zone_b = zones.split('-')

        # If metadata is found, save it in a dictionary for later use
        metadata: dict[str, ] = dict()
        if "[" in connection_line:
            extradata = connection_line.split("[")[-1].replace("]", "")
            print("This is extradata", extradata)
            key, value = extradata.split("=")
            if "max_link_capacity" not in key:
                raise exc.WrongMetadataFoundError(f"'{key}'"
                                              "metadata not supported")
            metadata[key] = int(value)

        # Create connection objct
        connection_obj = Connection(graph.get_zone(zone_a.strip()),
                                    graph.get_zone(zone_b.strip()),
                                    metadata.get("max_link_capacity", 1))

        # Add connection object to graph
        graph.add_connection(connection_obj)

    def main_parser(self, file_path: str):
        with open(file_path, "r") as map_file:
            # Creating graph

            # Zone checks for parser
            zone_check = ["start_hub:", "end_hub:", "hub:"]
            try:
                for line in map_file:
                    # Skip if line is empthy or starts with '# '
                    if not line or line.startswith("# "):
                        continue
                    # Uses nb_drones_parser
                    elif "nb_drones:" in line:
                        self.line_number += 1
                        self.nb_drones_parser(line, self.graph)
                    # Uses zone_parser if zone in zone_check
                    elif any(zone in line for zone in zone_check):
                        self.line_number += 1
                        self.zone_parser(line, self.graph)
                    # Uses connection parser
                    elif "connection:" in line:
                        self.line_number += 1
                        self.connection_parser(line, self.graph)

                # Check if we have start zone to create
                # drones and set their start zone
                if self.graph.start_zone.is_start:
                    start_zone = self.graph.start_zone.is_start
                    drone_count = self.graph.nb_drones_count
                    # Create a list of drones and add them to self.graph
                    for drone_id in range(1, (drone_count + 1)):
                        drone_obj = Drone(drone_id, start_zone)
                        self.graph.drones_list.append(drone_obj)
            except Exception as error:
                print(f"caught error during parsing: {error}")
                exit(1)

