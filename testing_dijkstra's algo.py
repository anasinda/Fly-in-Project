# import heapq

# dist_list = {}
# pq = []
# path = {}
# adjacency_list = {
#     'A': [[3, 'B'], [6, 'C'], [4, 'D']],
#     'B': [[2, 'C'], [3, 'E']],
#     'C': [[3, 'E'], [3, 'F']],
#     'D': [[6, 'F']],
#     'E': [[1, 'F']],
#     'F': []
# }

# for key in adjacency_list.keys():
#     dist_list[key] = float("inf")
# dist_list['A'] = 0

# heapq.heappush(pq, (dist_list['A'], 'A'))
# while pq:
#     distance, node = heapq.heappop(pq)
#     if distance > dist_list[node]:
#         continue
#     for weight, vertex in adjacency_list[node]:
#         new_dist = dist_list[node] + weight
#         if new_dist < dist_list[vertex]:
#             dist_list[vertex] = new_dist
#             path[vertex] = node
#             heapq.heappush(pq, (dist_list[vertex], vertex))

# # Create path by going to where each node came from list
# final_path = []
# current = 'F'
# while current is not None:
#     final_path.append(current)
#     current = path.get(current)

# final_path.reverse()
# print(path)
# print(final_path)
# print(dist_list)



# class Solution:
#     def shortestPath(self, n: int, edges: list[list[int]], src: int) -> dict[int, int]:
#         dist_list = {}
#         pq = []
#         adj_list = {}

#         for index in range(n):
#             dist_list[index] = float("inf")
#             adj_list[index] = []
#         dist_list[src] = 0

#         for u, v, w in edges:
#             adj_list[u].append([v, w])

#         heapq.heappush(pq, (dist_list[src], src))
#         while pq:
#             distance, node = heapq.heappop(pq)
#             if distance > dist_list[node]:
#                 continue
#             for vertex, weight in adj_list[node]:
#                 check_dist = dist_list[node] + weight
#                 if check_dist < dist_list[vertex]:
#                     dist_list[vertex] = check_dist
#                     heapq.heappush(pq, (dist_list[vertex], vertex))

#         for key, value in dist_list.items():
#             if value != float("inf"):
#                 continue
#             else:
#                 dist_list[key] = -1
#         return dist_list

# sol = Solution()
# dij = sol.shortestPath(n, edges, src)
# print(dij)
