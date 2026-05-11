from src.models.drone import Drone
from src.models.zone import Zone
from src.models.graph import Graph
from src.models.zone_types import ZoneType
import heapq


class Pathfinder:
    def __init__(self, graph: Graph):
        self.graph = graph

    def run_dijkstra_algo(self, start: Zone, end: Zone) -> list[Zone]:
        dist_list = {zone_name: float("inf") for zone_name in self.graph.zones.keys()}
        dist_list[start.zone_name] = 0




        # for key, value in dist_list.items():
        #     print(f"This is key: {key} --- This is value: {value}")


