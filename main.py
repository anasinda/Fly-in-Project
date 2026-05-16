from src.parsing.parser import Parser
from src.algorithms.pathfinding import Pathfinder
from src.models.graph import Graph
from src.models.zone import Zone
from src.models.drone import Drone
from src.algorithms.simulation import Simulator
from src.utils.drone_path_setter import DronePathSetter
from sys import argv

parser: Parser = Parser()
file_path: str = argv[1]
parser.main_parser(file_path)
map_graph: Graph = parser.graph
finder: Pathfinder = Pathfinder(map_graph)
shortest_path: list[Zone] = finder.run_dijkstra_algo(
    map_graph.zones[map_graph.start_zone.zone_name],
    map_graph.zones[map_graph.end_zone.zone_name])
drone_path_setter: DronePathSetter = DronePathSetter(map_graph,
                                                     shortest_path,
                                                     map_graph.drones_list)
drone_path_setter.set_drones_path()
simulator: Simulator = Simulator(map_graph,
                                 shortest_path,
                                 map_graph.drones_list)

run_sim = simulator.run_simulation()
print(f"This is turns: {run_sim}")

