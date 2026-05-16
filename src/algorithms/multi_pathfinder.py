from src.models.graph import Graph
from src.models.zone import Zone
from src.utils.exceptions import NoPathFoundError
from src.algorithms.pathfinding import Pathfinder

class MultiPathfinder:
    def __init__(self, graph: Graph, pathfinder: Pathfinder) -> None:
        self.graph = graph
        self.pathfinder = pathfinder
        self.paths: list[list[Zone]]
        self.previuos_path: list[Zone] | None = None

    @staticmethod
    def find_best_paths(path: list[Zone]) -> int:
        return min(zone.zone_capacity for zone in path)

    def run_multi_pathfinder(self) -> list[list[Zone]]:
        while True:
            try:
                current_path = self.pathfinder.run_dijkstra_algo(
                    self.graph.start_zone, self.graph.end_zone)
                if current_path == self.previuos_path:
                    break
                self.paths.append(current_path)
                for zone in current_path:
                    zone.increase_zone_cost()
                self.previuos_path = current_path
            except NoPathFoundError:
                break

        for path in self.paths:
            for zone in path:
                zone.decrease_zone_cost()

        self.paths.sort(key=self.find_best_paths(), reverse=True)
        return self.paths
