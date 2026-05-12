from src.parsing.parser import Parser
from src.algorithms.pathfinding import Pathfinder
from sys import argv

parser = Parser()
file_path = argv[1]
parser.main_parser(file_path)
finder = Pathfinder(parser.graph)
path = finder.run_dijkstra_algo(
    parser.graph.zones['start'],
    parser.graph.zones['goal'])
path_names = [p.zone_name for p in path]
print(path_names)
