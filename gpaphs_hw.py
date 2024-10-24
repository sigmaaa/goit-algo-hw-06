import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def bfs_iterative(graph, start, looking_vertex):
    visited = set()
    queue = deque([start])

    while (queue):
        vertex = queue.popleft()
        if vertex == looking_vertex:
            return visited
        if vertex not in visited:
            visited.add(vertex)
            print(vertex)
            queue.extend(set(graph[vertex]) - visited)
    return -1


def dfs_iterative(graph, start, looking_vertex):
    visited = set()
    stack = [start]
    while (stack):
        vertex = stack.pop()
        if vertex == looking_vertex:
            return visited
        if vertex not in visited:
            visited.add(vertex)
            print(vertex)
            stack.extend(reversed(graph[vertex]))
    return -1


def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # Щоб зберігати попередників для відтворення шляху
    previous_vertices = {vertex: None for vertex in graph}

    unvisited = list(graph.keys())

    while unvisited:
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        if distances[current_vertex] == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex] + weight

            # Оновлюємо найкоротшу відстань, якщо знайдено коротший шлях
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Запам'ятовуємо попередника
                previous_vertices[neighbor] = current_vertex

        unvisited.remove(current_vertex)

    return distances, previous_vertices


def restore_path(vertices_map, looking_vertex):
    path = []
    while vertices_map.get(looking_vertex) is not None:
        path.append(looking_vertex)
        looking_vertex = vertices_map.get(looking_vertex)
    path.append(looking_vertex)
    path.reverse()
    return path


weight_transport_network = {
    "A": {"B": 4, "C": 3},
    "B": {"A": 4, "D": 2},
    "C": {"A": 3, "E": 5},
    "D": {"B": 2, "F": 1},
    "E": {"C": 5, "F": 6},
    "F": {"D": 1, "E": 6, "G": 2, "H": 2},
    "G": {"F": 2, "H": 2},
    "H": {"F": 2, "G": 2}
}


def print_network(transport_network):
    G = nx.Graph(transport_network)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=500,
            node_color="skyblue", font_size=10, font_weight="bold")
    edge_labels = {(key, inner_key): weight_transport_network[key][inner_key]
                   for key in weight_transport_network for inner_key
                   in weight_transport_network[key]}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color="gray")
    plt.title("Транспортна мережа міста")
    plt.show()

    # Аналіз характеристик
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    degree_centrality = dict(G.degree())

    print(f"Кількість станцій (вершин): {num_nodes}")
    print(f"Кількість маршрутів (ребер): {num_edges}")
    print("Ступені вершин (станції):")

    for station, degree in degree_centrality.items():
        print(f"Станція {station}: {degree} маршрутів")


print_network(weight_transport_network)
print("____________BFS:______________")
print(bfs_iterative(weight_transport_network, 'A', 'H'))
print("____________DFS:______________")
print(dfs_iterative(weight_transport_network, 'A', 'H'))


distances, vertices = dijkstra(weight_transport_network, 'A')
print(distances)
for vertex in vertices:
    print(f"shortest path for {vertex}")
    print(restore_path(vertices, vertex))
