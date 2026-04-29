from models.connection import Connection
from models.drone import Drone
from models.graph import Graph
from models.zone_types import ZoneType
from models.zone import Zone
from utils.exceptions import *

class Parser:
    def __init__(self):
        self.graph: Graph = Graph()
        self.line_number: int = 0
        self.check_list:dict[str, bool] = {
            "nb_drones": False,
            "start_hub": False,
            "end_hub": False
        }

    def nb_drones_parser(self, drones_line: str, our_graph:Graph) -> None:

        #Split line, and remove ':'
        nb_drones, drone_count = drones_line.split()
        nb_drones = nb_drones.replace(":", "")

        # Check if value is a number
        if not drone_count.isdigit():
            raise ValueError(f"{drone_count} is not a number")

        #Turn string number to integer number
        drone_count = int(drone_count)

        #Check if we already have nb_drones
        if self.check_list[nb_drones]:
            raise DuplicateDroneCountLineError("Found duplicate"
                                               f"{nb_drones} at line"
                                               f"{self.line_number}")

        #Check if value is negative or zero
        elif drone_count <= 0:
            raise ValueError(f"Drone count {drone_count} not acceptable")

        #Set nb_drones as found and register it
        self.check_list[nb_drones] = True
        our_graph.nb_drones = drone_count

        #Create drones and add them to dictionary based on their ID
        # for drone in range(1, drone_count + 1):
        #     drone_obj = Drone(drone)
        #     all_drones[drone_obj.full_drone_id] = drone_obj


    def zone_parser(self, zone: str, our_graph: Graph) -> None:
            #Split line, and remove ":" from zone_ype
            main_data = zone.split("[")[0]
            zone_type, zone_name, x, y = main_data.split()
            zone_type = zone_type.replace(":", "")

            #Check if x and y are digits
            if not x.isdigit() or not y.isdigit():
                raise ValueError(f"{x} or {y} is not  number")

            #Turn x and y charachter values to integer values
            x, y = map(int, [x, y])

            #Split metadata and save it in a dictionary
            metadata = dict()
            if "[" in zone:
                extradata = zone.replace("[", "")[1].replace("]", "")
                for data in extradata.split():
                    key, value = data.split("=")
                    metadata[key] = value

                #Use metadata and set default values if not found
                zone_color: str = metadata.get("color", None)
                zone_capacity: str = metadata.get("max_drones", 1)

                #Check if zone capacity is an integer
                if not zone_capacity.isdigit():
                    raise ValueError(f"{zone_capacity} is not  number")
                zone_capacity = int(zone_capacity)

                #Check zone_type exists
                try:
                    zone_type = ZoneType(metadata.get("zone", "normal"))
                except ValueError:
                    raise ZoneTypeError(f"{self.line_number}:"
                                     f"invalid zone type '{metadata['zone']}'")

                #Creating zone object
                zone_obj = Zone(x, y, zone_name, zone_type, zone_color, zone_capacity)

                #Checking if zone is start or end
                if zone_type == "start_hub":
                    zone_obj.is_start = True
                elif zone_type == "end_hub":
                    zone_obj.is_end = True

                #Adding zone to zones dictionray in our graph
                our_graph.zones[zone_name] = zone_obj


    def connection_parser(self, connection_line: str, our_graph:Zone) -> None:
        connection, zones = connection_line.split("[")
        connection.replace(":", "")
        zone_a, zone_b = zones.split('-')

        metadata: dict[str, ] = dict()
        if "[" in connection_line:
            metadata



    def main_parser(self, file_path: str):
        with open(file_path, "r") as map_file:
            # all_drones:dict[str, Drone] = dict()
            our_graph = Graph()
            zone_check = ["start_hub:", "end_hub:", "hub:"]
            for line in map_file:
                if not line or line.startswith("#"):
                    continue
                elif "nb_drones:" in line:
                    self.line_number += 1
                    self.nb_drones_parser(line, our_graph)
                elif any(zone in line for zone in zone_check):
                    self.line_number += 1
                    self.zone_parser(line, our_graph)
                elif "connection:" in line:
                    self.line_number += 1
                    self.connection_parser(line, our_graph)

