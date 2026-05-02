from models.connection import Connection
from models.drone import Drone
from models.graph import Graph
from models.zone_types import ZoneType
from models.zone import Zone
import utils.exceptions as exc
from typing import Any


class Parser:
    def __init__(self):
        self.graph: Graph = Graph()
        self.line_number: int = 0

    def nb_drones_parser(self, drones_line: str, graph: Graph) -> None:

        # Split line, and remove ':'
        nb_drones, drone_count = drones_line.split()
        nb_drones = nb_drones.replace(":", "")

        # Check if value is a number
        if not drone_count.isdigit():
            raise ValueError(f"{drone_count} is not a number")

        # Turn string number to integer number and check if negative or zero
        drone_count = int(drone_count)
        if drone_count <= 0:
            raise ValueError(f"Drone count {drone_count} not acceptable")

        # Check if we already have nb_drones
        if graph.nb_drones_check:
            raise exc.DuplicateDroneCountLineError("Found duplicate"
                                                   f"{nb_drones} at line"
                                                   f"{self.line_number}")

        # Set nb_drones as found and register it
        graph.nb_drones_check = True
        graph.nb_drones_count = drone_count

    def zone_parser(self, zone: str, graph: Graph) -> None:
        # Split line, and remove ":" from zone_ype
        main_data = zone.split("[")[0]
        zone_type, zone_name, x, y = main_data.split()
        zone_type = zone_type.replace(":", "")

        # Check if start or end zone is a duplicate
        if self.check_list[zone_type]:
            raise exc.DuplicateStartOrEndZoneError(
                f"Found duplicate {zone_type}")

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
            extradata = zone.replace("[", "")[1].replace("]", "")
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

                # Check zone_type exists
                try:
                    zone_type = ZoneType(metadata.get("zone", "normal"))
                except ValueError:
                    raise exc.ZoneTypeError(f"{self.line_number}:"
                                            "invalid zone type"
                                            f"'{metadata['zone']}'")

                # Creating zone object
                zone_obj = Zone(x, y,
                                zone_name,
                                zone_type,
                                zone_color,
                                zone_capacity)

                # Checking if zone is start or end
                if zone_type == "start_hub":
                    zone_obj.is_start = True
                elif zone_type == "end_hub":
                    zone_obj.is_end = True
                # Adding zone to zones dictionray in our graph
                graph.add_zone(zone_obj)

    def connection_parser(self,
                          connection_line: str,
                          graph: Graph) -> None:
        # Split line, only take two parts, remove ':', split zone connections
        zones = connection_line.split("", 1)[1]
        #  connection.replace(":", "")
        zone_a, zone_b = zones.split('-')

        # If metadata is found, save it in a dictionary for later use
        metadata: dict[str, ] = dict()
        if "[" in connection_line:
            extradata = connection_line.split("[")[-1].replace("]", "")
            key, value = extradata.split("-")
            metadata[key] = value

        # Create connection objct
        connection_obj = Connection(graph.get_zone(zone_a),
                                    graph.get_zone(zone_b),
                                    metadata["max_link_capacity"])

        # Add connection object to graph
        graph.add_connection(connection_obj)

    def main_parser(self, file_path: str):
        with open(file_path, "r") as map_file:
            # Creating graph

            # Zone checks for parser
            zone_check = ["start_hub:", "end_hub:", "hub:"]
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
