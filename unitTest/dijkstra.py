# Testing of algorithm.
# Comparing dijsktra algorithm with own.
# This is dijsktra algorithm.
import timeit

import heapq
def dijkstra(x, start, target=None):
    # Build adjacency list from your data structure
    graph = {}
    for u, v, w in zip(x[0], x[1], x[2]):
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))  # undirected graph
    # Initialize distances and predecessors
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    # Priority queue (min-heap)
    pq = [(0, start)]
    while pq:
        current_dist, u = heapq.heappop(pq)
        # If we reached the target, we can stop early
        if target and u == target:
            break
        if current_dist > dist[u]:
            continue
        # Loop through neighbors
        for v, w in graph[u]:
            new_dist = dist[u] + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))
    # If target specified, reconstruct path
    if target:
        path = []
        node = target
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        return dist[target], path
    return dist, prev


# Example usage with your data
x = [
    ["A", "A", "A", "B", "B", "B", "C", "C", "D", "D", "E"],
    ["B", "F", "D", "F", "E", "C", "E", "G", "E", "G", "G"],
    [2, 3, 5, 4, 1, 7, 3, 4, 1, 1, 3]
]

# Find shortest path from A to C
elapsed = timeit.timeit(lambda: dijkstra(x, start="A", target="B"))
distance, path = dijkstra(x, start="A", target="F")
print("Shortest distance:", distance)
print("Path:", path)
print(elapsed)