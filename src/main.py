from parser import Parser
from sys import argv

parser = Parser()
file_path = argv[1]
parser.main_parser(file_path)
print("File path:", file_path)
print("Drone list:", parser.graph.drones_list)
print("Do drones exist:", parser.graph.nb_drones_check)
print("Drone count:", parser.graph.nb_drones_count)
print("Len of dictionaray of zones:", len(parser.graph.zones))
