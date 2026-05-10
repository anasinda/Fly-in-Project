import heapq

adjacency_list = {
    'A': [['B', 3], ['C', 6], ['D', 4]],
    'B': [['C', 2], ['E', 3]],
    'C': [['E', 3], ['F', 3]],
    'D': [['F', 6]],
    'E': [['F', 1]],
    'F': []
}


dist_list = dict()
unvisited = []
path = []
start = 'A'
pq = []

for key in adjacency_list:
    dist_list[key] = float('inf')
    unvisited.append(key)
dist_list[start] = 0

heapq.heappush(pq, (dist_list[start], start))


while pq:
    distance, node = heapq.heappop(pq)
    if distance > dist_list[node]:
        continue
    for neighbor, weight in adjacency_list[node]:
        if dist_list[node] + weight < dist_list[neighbor]:
            dist_list[neighbor] = dist_list[node] + weight
            heapq.heappush(pq, (dist_list[neighbor], neighbor))
print(dist_list)
