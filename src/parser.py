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

    def nb_drones_parser(self,
                         drones_line: str,
                         all_drones: dict[str, Drone]) -> dict[str, Drone]:
        nb_drones, drone_count = drones_line.split()
        nb_drones = nb_drones.replace(":", "")
        drone_count = int(drone_count)
        if self.check_list[nb_drones]:
            raise DuplicateDroneCountLineError("Found duplicate"
                                               f"{nb_drones} at line"
                                               f"{self.line_number}")
        elif drone_count <= 0:
            raise ValueError(f"Drone count {drone_count} not acceptable")
        self.check_list[nb_drones] = True

        for drone in range(1, drone_count + 1):
            drone_obj = Drone(drone)
            all_drones[drone_obj.full_drone_id] = drone_obj

    # def start_end_hub_parser(self, start_end_hub: str) -> None:
    #         start__end_hub_list = start_end_hub.split("", 4)
    #         start_end_hub_metadata: = start__end_hub_list[4]



    def main_parser(self, file_path: str):
        with open(file_path, "r") as map_file:
            all_drones:dict[str, Drone] = dict()
            for line in map_file:
                if not line or line.startswith("#"):
                    continue
                elif "nb_drones:" in line:
                    self.line_number += 1
                    self.nb_drones_parser(line, all_drones)
                elif "start_hub:" in line or "end_hub:" in line:
                    self.line_number += 1
                    self.start_end_hub_parser(line)
