from src.models.drone import Drone
from src.models.zone import Zone
from src.models.graph import Graph

class Pathfinder:
    def __init__(self, graph: Graph):
        self.graph = graph

    def run_dijkstra_algo(self):
        zones: dict[str, Zone] = self.graph.zones
        dist_list: dict[str, int | float] = dict()

        for name, zone in zones.items():
            if zone.is_start:
                dist_list[name] = 0
            else:
                dist_list[name] = float('inf')

        for key, value in dist_list.items():
            print(f"This is key: {key} --- This is value: {value}")
