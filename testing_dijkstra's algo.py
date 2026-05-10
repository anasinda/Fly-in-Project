import heapq

# adjacency_list = {
#     'A': [['B', 3], ['C', 6], ['D', 4]],
#     'B': [['C', 2], ['E', 3]],
#     'C': [['E', 3], ['F', 3]],
#     'D': [['F', 6]],
#     'E': [['F', 1]],
#     'F': []
# }


# dist_list = dict()
# unvisited = []
# path = []
# start = 'A'
# pq = []

# for key in adjacency_list:
#     dist_list[key] = float('inf')
#     unvisited.append(key)
# dist_list[start] = 0

# heapq.heappush(pq, (dist_list[start], start))


# while pq:
#     distance, node = heapq.heappop(pq)
#     if distance > dist_list[node]:
#         continue
#     for neighbor, weight in adjacency_list[node]:
#         if dist_list[node] + weight < dist_list[neighbor]:
#             dist_list[neighbor] = dist_list[node] + weight
#             heapq.heappush(pq, (dist_list[neighbor], neighbor))
# print(dist_list)


# number of vertexs
n = 5

# 0 == source/where the node starts  --- vertex/node/u
# 1 == destination/where to go from the source to this using
###### weight/edge --- vertex/node/v
# 10 == weight/cost/edge
edges = [[0,1,10], [0,2,3], [1,3,2], [2,1,4], [2,3,8], [2,4,2], [3,4,5]]

# source vertex from where we start the algo
src = 0

from copy import deepcopy
from copy import copy

class Solution:
    def shortestPath(self, n: int, edges: list[list[int]], src: int) -> dict[int, int]:


        dist_list = {}
        pq = []
        adj_list = {}
        # edges_copy = deepcopy(edges)

        for index in range(n):
            dist_list[index] = float("inf")
        dist_list[src] = 0
        print(dist_list)

        for u, v, w in edges:
            if u in adj_list:
                adj_list[u].append([v, w])
            else:
                adj_list[u] = [[v, w]]
        print(adj_list)

        heapq.heappush(pq, (dist_list[src], src))
        # for element in edges_copy:
        #     key = element.pop(0)
        #     value = element
        #     if key in adj_list:
        #         adj_list[key].append(value)
        #     else:
        #         adj_list[key] = [value]

        # for v, _ in edges_copy:
        #     if v not in adj_list:
        #         adj_list[v] = []

        # for vertex in edges:
        #     dist_list[vertex[0]] = float("inf")
        #     if vertex[1] not in dist_list:
        #         dist_list[vertex[1]] = float("inf")
        # dist_list[src] = 0
        # heapq.heappush(pq, (src, dist_list[src]))

        # while pq:
        #     vertex, distance = heapq.heappop(pq)
        #     if distance > dist_list[vertex]:
        #         continue
        #     for neighbor, weight in adj_list[vertex]:
        #         if dist_list[vertex] + weight < dist_list[neighbor]:
        #             dist_list[neighbor] = dist_list[vertex] + weight
        #             heapq.heappush(pq, (neighbor, dist_list[neighbor]))
        # return dist_list



sol = Solution()
dij = sol.shortestPath(n, edges, src)
print(dij)
