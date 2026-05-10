from src.parsing.parser import Parser
from src.algorithms.pathfinding import Pathfinder
from sys import argv

parser = Parser()
file_path = argv[1]
parser.main_parser(file_path)
print("File path:", file_path)
print("Drone list:", parser.graph.drones_list)
print("Do drones exist:", parser.graph.nb_drones_check)
print("Drone count:", parser.graph.nb_drones_count)
print("Len of dictionaray of zones:", len(parser.graph.zones))

for name, connection in parser.graph.adjacency.items():
    print(f"zone name: {name}")
    for con in connection:
        print("This is connectin in list:", con)
        print("This is zone_a:", con.zone_a.zone_name)
        print("This is zone_b:", con.other_zone(con.zone_a.zone_name).zone_name)

print("")
print("")
finder = Pathfinder(parser.graph)
finder.run_dijkstra_algo()
