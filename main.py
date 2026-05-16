from sys import argv
from src.models.graph import Graph
from src.parsing.parser import Parser
from src.algorithms.pathfinding import Pathfinder
from src.utils.drone_path_setter import DronePathSetter
from src.algorithms.simulation import Simulator


graph = Graph()
parser = Parser(graph)
parser.run_parser()
pathfinder = Pathfinder(graph)
find_path = pathfinder.run_dijkstra_algo(graph.start_zone, graph.end_zone)
drone_path_setter = DronePathSetter(find_path, graph.drones_list)
drone_path_setter.set_drones_path()
simulator = Simulator(graph, find_path, graph.drones_list)
print(simulator.run_simulation())
print(graph.nb_drones_count)
