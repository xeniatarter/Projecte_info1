from path import find_shortest_path
from graph import CreateGraph_1, CreateGraph_2
from node import Node


def test_find_shortest_path(graph, start_name, end_name, expected_path):
    path = find_shortest_path(graph, start_name, end_name)

    assert path == expected_path, f"Error: Expected {expected_path}, but got {path}" #Comprobamos si el camino obtenido es el esperado
    print(f"Test passed for path from {start_name} to {end_name}: {path}")

def run_tests(): #Creamos gráficos de ejemplo
    graph1 = CreateGraph_1()
    graph2 = CreateGraph_2()

    test_find_shortest_path(graph1, "A", "D", ["A", "B", "C", "D"])  #Camino más corto entre dos nodos en CreateGraph_1
    test_find_shortest_path(graph1, "F", "L", ["F", "L"])

    test_find_shortest_path(graph2, "MAD", "STC", ["MAD", "PMA", "STC"])  # Camino más corto entre dos nodos en CreateGraph_2
    test_find_shortest_path(graph2, "SEV", "BCN", ["SEV", "VCN", "BCN"])

    print("All tests passed!")


run_tests() #Ejecutar test
