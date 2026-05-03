from parser import Parser
from sys import argv

parser = Parser()
file_path = argv[1]
print(file_path)
parser.main_parser(file_path)
print(parser.graph.drones_list)
print(parser.graph.nb_drones_check)
print(parser.graph.nb_drones_count)
print(parser.graph.zones["waypoint1"].zone_name)
