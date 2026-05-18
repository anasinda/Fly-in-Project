from src.models.graph import Graph
from src.models.zone import Zone
from src.utils.exceptions import NoPathFoundError
from src.algorithms.pathfinding import Pathfinder

class MultiPathfinder:
    def __init__(self, graph: Graph, pathfinder: Pathfinder) -> None:
        self.graph = graph
        self.pathfinder = pathfinder
        self.paths: list[list[Zone]] = []
        self.previuos_path: list[Zone] | None = None

    def run_multi_pathfinder(self) -> list[list[Zone]]:

        while True:
            try:
                current_path = self.pathfinder.run_dijkstra_algo(self.graph.start_zone, self.graph.end_zone)
                if current_path in self.paths:
                    break
                self.paths.append(current_path)
                for zone in current_path:
                    zone.increase_zone_cost()
            except NoPathFoundError:
                print("HERE")
                break

        for path in self.paths:
            for zone in path:
                zone.decrease_zone_cost()
        return self.paths


