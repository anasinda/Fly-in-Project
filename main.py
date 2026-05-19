from src.models.zone import Zone
from src.models.graph import Graph
from src.parsing.parser import Parser
from src.algorithms.pathfinding import Pathfinder
from src.algorithms.multi_pathfinder import MultiPathfinder
from src.utils.drone_path_setter import DronePathSetter
from src.algorithms.simulation import Simulator

try:
    graph = Graph()
    parser = Parser(graph)
    parser.run_parser()
    pathfinder = Pathfinder(graph)
    multi_pathfinder = MultiPathfinder(graph, pathfinder)
    multi_paths: list[list[Zone]] = multi_pathfinder.run_multi_pathfinder()
    drone_path_setter = DronePathSetter(multi_paths, graph.drones_list)
    drone_path_setter.set_drones_path()
    simulator: int = Simulator(graph, graph.drones_list)
    simulator.run_simulation()
except KeyboardInterrupt as k_e:
    print("Exited program with Ctrl + C")
except Exception as e:
    print(e)
