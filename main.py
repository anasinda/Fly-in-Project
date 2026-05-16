from sys import argv
from src.models.zone import Zone
from src.models.graph import Graph
from src.parsing.parser import Parser
from src.algorithms.pathfinding import Pathfinder
from src.algorithms.multi_pathfinder import MultiPathfinder
from src.utils.drone_path_setter import DronePathSetter
from src.algorithms.simulation import Simulator


def path_generator(paths: list[list[Zone]], graph: Graph) -> dict[str, list[Zone]]:
    
    # path_holder: dict[str, list[Zone] | int] = {}
    # first_path: list[Zone] = pathfinder.run_dijkstra_algo(graph.start_zone, graph.end_zone)

    # for zone in first_path:
    #     zone.increase_zone_cost()

    # second_path: list[Zone] = pathfinder.run_dijkstra_algo(graph.start_zone, graph.end_zone)
    # first_path_bottleneck = min(zone.zone_capacity for zone in first_path)
    # second_path_bottleneck = min(zone.zone_capacity for zone in second_path)

    # # for zone in first_path:
    # #     zone.decrease_zone_cost()

    # if first_path == second_path:
    #     path_holder['best_path'] = first_path
    #     path_holder['longer_path'] = None
    # elif first_path_bottleneck > second_path_bottleneck:
    #     path_holder['best_path'] = first_path
    #     path_holder['longer_path'] = second_path
    # elif second_path_bottleneck > first_path_bottleneck:
    #     path_holder['best_path'] = second_path
    #     path_holder['longer_path'] = first_path
    # else:
    #     if len(first_path) < len(second_path):
    #         path_holder['best_path'] = first_path
    #         path_holder['longer_path'] = second_path
    #     else:
    #         path_holder['best_path'] = second_path
    #         path_holder['longer_path'] = first_path

    # print(f"first path bottleneck", first_path_bottleneck)
    # print(f"second path bottleneck", second_path_bottleneck)
    # path_holder['first_path'] = first_path_bottleneck
    # path_holder['second_path'] = second_path_bottleneck

    # return path_holder





graph = Graph()
parser = Parser(graph)
parser.run_parser()
pathfinder = Pathfinder(graph)
multi_pathfinder = MultiPathfinder(graph, pathfinder)
paths = multi_pathfinder.run_multi_pathfinder()
paths_generated: dict[str, list[Zone] | int] = path_generator(pathfinder, graph)
drone_path_setter = DronePathSetter(paths_generated, graph.drones_list)
drone_path_setter.set_drones_path()
simulator = Simulator(graph, graph.drones_list)
print(simulator.run_simulation())
print(graph.nb_drones_count)
