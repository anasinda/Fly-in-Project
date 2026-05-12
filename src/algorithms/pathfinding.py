from src.models.zone import Zone
from src.models.graph import Graph
from src.models.connection import Connection
from src.utils.exceptions import BlockedZoneError, NoPathFoundError
import heapq


class Pathfinder:
    def __init__(self, graph: Graph) -> None:
        """
        Initializing graph as attribute of pathfinder class
        """
        self.graph: Graph = graph

    def run_dijkstra_algo(self, start: Zone, end: Zone) -> list[Zone]:
        """
        Dijkstra's algorithm for finding the shortest path
        our drones can take to reach the end/goal zone
        """
        dist_list: dict[str, float] = {
            zone_name: float("inf") for zone_name in self.graph.zones.keys()
        }
        dist_list[start.zone_name] = 0
        previous: dict[str, str | None] = {
            zone_name: None for zone_name in self.graph.zones.keys()
        }
        queue: list[tuple[float, str]] = [(dist_list[start.zone_name],
                                         start.zone_name)]
        path: list[Zone] = []

        while queue:
            cost, current_zone = heapq.heappop(queue)
            if cost > dist_list[current_zone]:
                continue
            connections: list[Connection] = self.graph.get_zone_connections(
                current_zone
            )
            for connection in connections:
                other_zone: Zone = connection.other_zone(current_zone)
                try:
                    move_cost: int = other_zone.zone_move_cost()
                    new_cost = cost + move_cost
                    if new_cost < dist_list[other_zone.zone_name]:
                        dist_list[other_zone.zone_name] = new_cost
                        previous[other_zone.zone_name] = current_zone
                        heapq.heappush(queue, (new_cost, other_zone.zone_name))
                except BlockedZoneError:
                    continue

        if dist_list[end.zone_name] == float("inf"):
            raise NoPathFoundError

        current: str | None = end.zone_name
        while current is not None:
            path.append(self.graph.get_zone(current))
            current = previous[current]
        path.reverse()
        return path
