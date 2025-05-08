from node import Node
from segment import Segment

def find_shortest_path(graph, start_name, end_name):
    start_node = next((n for n in graph.nodes if n.name == start_name), None)
    end_node = next((n for n in graph.nodes if n.name == end_name), None)

    if not start_node or not end_node:
        return None

    # Inicializar distancias
    unvisited = {node: float('inf') for node in graph.nodes}
    previous_nodes = {}
    unvisited[start_node] = 0

    while unvisited:
        current_node = min(unvisited, key=unvisited.get)
        current_distance = unvisited[current_node]

        if current_node == end_node:
            break

        for segment in graph.segments:
            # SOLO permitimos la dirección origin -> destination
            if segment.origin == current_node:
                neighbor = segment.destination
                if neighbor in unvisited:
                    new_distance = current_distance + segment.cost
                    if new_distance < unvisited[neighbor]:
                        unvisited[neighbor] = new_distance
                        previous_nodes[neighbor] = current_node

        unvisited.pop(current_node)

    # Reconstruir el camino
    path = []
    current = end_node
    while current != start_node:
        if current not in previous_nodes:
            return None  # No hay camino válido
        path.insert(0, current)
        current = previous_nodes[current]
    path.insert(0, start_node)
    return path





