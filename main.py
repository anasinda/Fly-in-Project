from src.models.zone import Zone
from src.models.graph import Graph
from src.parsing.parser import Parser
from src.algorithms.pathfinding import Pathfinder
from src.algorithms.multi_pathfinder import MultiPathfinder
from src.utils.drone_path_setter import DronePathSetter
from src.algorithms.simulation import Simulator
from src.display.visualization import Visualizer
from src.utils.exceptions import NoPathFoundError


try:
    graph = Graph()
    parser = Parser(graph)
    parser.run_parser()
    pathfinder = Pathfinder(graph)
    multi_pathfinder = MultiPathfinder(graph, pathfinder)
    multi_paths: list[list[Zone]] = multi_pathfinder.run_multi_pathfinder()
    drone_path_setter = DronePathSetter(multi_paths, graph.drones_list)
    drone_path_setter.set_drones_path()
    simulator = Simulator(graph, graph.drones_list)
    simulator_results: tuple[int, list[list[str]]] = simulator.run_simulation()
    visualization = Visualizer(graph,
                               simulator_results[0],
                               simulator_results[1])
    visualization.run()
except KeyboardInterrupt:
    print("\rExited program with Ctrl + C")
except NoPathFoundError as e:
    print(e)
    exit(1)
