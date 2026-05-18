import sys
import matplotlib.pyplot as plt
import networkx as nx

def prim_algorithm_terminal_and_visual(matrix):
    num_vertices = len(matrix)
    
    selected_vertices = [False] * num_vertices
    selected_vertices[0] = True
    
    num_edges = 0
    mst_edges = []
    total_weight = 0

    print("=" * 50)
    print("        АЛГОРИТМ ПРІМА: ПОБУДОВА СТОВБУРА")
    print("=" * 50)
    
    print("\n[1] СПИСОК УСІХ РЕБЕР ВХІДНОГО ГРАФА:")
    print(f"{'Ребро':<12} | {'Вага':<6}")
    print("-" * 23)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if matrix[i][j] > 0:
                print(f"e(V{i+1}, V{j+1})  | {matrix[i][j]}")

    print("\n[2] ПОКРОКОВИЙ ВИБІР РЕБЕР ДО СТОВБУРА:")
    print(f"{'Крок':<6} | {'Обране ребро':<15} | {'Вага ребра':<10}")
    print("-" * 38)

    while num_edges < num_vertices - 1:
        minimum = sys.maxsize
        u = 0
        v = 0
        
        for i in range(num_vertices):
            if selected_vertices[i]:
                for j in range(num_vertices):
                    if not selected_vertices[j] and matrix[i][j]:  
                        if minimum > matrix[i][j]:
                            minimum = matrix[i][j]
                            u = i
                            v = j
                            
        selected_vertices[v] = True
        num_edges += 1
        total_weight += minimum
        mst_edges.append((u, v, minimum))
        
        print(f"Крок {num_edges:<1} | e(V{u+1}, V{v+1}){' ':<7} | {minimum:<10}")
        
    print("\n" + "=" * 50)
    print("[3] РЕЗУЛЬТАТ: МІНІМАЛЬНИЙ СТОВБУР ПОБУДОВАНО")
    print("=" * 50)
    print(f"{'Ребро стовбура':<18} | {'Вага':<6}")
    print("-" * 29)
    for u, v, weight in mst_edges:
        print(f"e(V{u+1}, V{v+1}){' ':<10} | {weight}")
    print("-" * 29)
    print(f"ЗАГАЛЬНА ВАГА СТОВБУРА: {total_weight}")
    print("=" * 50)

    G = nx.Graph()

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if matrix[i][j] > 0:
                G.add_edge(i, j, weight=matrix[i][j])

    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color="#98FB98", node_size=800, edgecolors="#333")
    labels = {i: f"V{i+1}" for i in range(num_vertices)}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=11, font_weight="bold")

    mst_edges_pairs = [(u, v) for u, v, _ in mst_edges]
    all_edges = list(G.edges())
    
    mst_edges_set = set(mst_edges_pairs) | set((v, u) for u, v in mst_edges_pairs)
    other_edges = [e for e in all_edges if e not in mst_edges_set]

    nx.draw_networkx_edges(G, pos, edgelist=other_edges, width=1.5, alpha=0.3, edge_color="gray", style="dashed")
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges_pairs, width=4, alpha=1.0, edge_color="red")

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color="black")

    plt.title(f"Мінімальний стовбур графа (Алгоритм Пріма)\nЧервоні лінії = Стовбур (Вага: {total_weight})", fontsize=12, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

graph_matrix = [
    [0, 9, 75, 14, 20],   # Ребра від V1
    [9, 0, 95, 19, 42],   # Ребра від V2
    [75, 95, 0, 51, 66],  # Ребра від V3
    [14, 19, 51, 0, 31],  # Ребра від V4
    [20, 42, 66, 31, 0]   # Ребра від V5
]

prim_algorithm_terminal_and_visual(graph_matrix)