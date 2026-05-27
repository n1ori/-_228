import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def partition_and_visualize():
    initial_graph_data = {
        1: {2, 4, 5, 6, 7, 8, 10, 16},
        2: {1, 5, 6, 7, 10},
        3: {4, 7, 11, 16},
        4: {1, 3, 9},
        5: {1, 2, 9},
        6: {1, 2, 10},
        7: {1, 2, 3, 11, 14, 12, 13},
        8: {1, 14, 15, 16},
        9: {4, 5, 10, 13, 11, 12, 14},
        10: {1, 2, 6, 9, 15, 11, 12, 13},
        11: {3, 7, 9, 10, 14, 15},
        12: {7, 9, 10, 14, 15, 16},
        13: {7, 9, 10, 15, 14, 16},
        14: {7, 8, 9, 11, 12, 13, 15, 16},
        15: {8, 10, 11, 12, 13, 14, 16},
        16: {1, 3, 8, 12, 13, 14, 15}
    }

    graph = {k: set(v) for k, v in initial_graph_data.items()}
    forbidden_vertices = [7, 14, 15]

    total_vertices = len(graph)
    num_chunks = len(forbidden_vertices)
    base_size = total_vertices // num_chunks
    remainder = total_vertices % num_chunks

    chunk_sizes = [base_size + (1 if i < remainder else 0) for i in range(num_chunks)]
    chunks = []

    for i, anchor in enumerate(forbidden_vertices):
        target_size = chunk_sizes[i]
        current_chunk = [anchor]

        while len(current_chunk) < target_size:
            candidates = set()
            for v in current_chunk:
                if v in graph:
                    for neighbor in graph[v]:
                        if neighbor not in current_chunk and neighbor not in forbidden_vertices:
                            candidates.add(neighbor)

            if not candidates:
                remaining_nodes = [k for k in graph.keys() if k not in current_chunk and k not in forbidden_vertices]
                if remaining_nodes:
                    candidates.add(remaining_nodes[0])
                else:
                    break

            best_vertex = -1
            min_weight = math.inf

            for candidate in candidates:
                rho = len(graph[candidate])
                a_ik = sum(1 for n in graph[candidate] if n in current_chunk)
                delta = rho - a_ik

                if delta < min_weight:
                    min_weight = delta
                    best_vertex = candidate
                elif delta == min_weight:
                    if len(graph[candidate]) > len(graph[best_vertex]):
                        best_vertex = candidate

            if best_vertex != -1:
                current_chunk.append(best_vertex)

        chunks.append(current_chunk)

        for v in current_chunk:
            if v in graph:
                del graph[v]
        for k in graph:
            graph[k] = {n for n in graph[k] if n not in current_chunk}

    print("=== РЕЗУЛЬТАТ РОЗБИТТЯ ===")
    for idx, chunk in enumerate(chunks):
        print(f"Шматок G_{idx + 1}: {sorted(chunk)}")

    # --- Етап побудови та візуалізації графа ---
    G = nx.Graph()
    for node, neighbors in initial_graph_data.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Визначаємо кольори для кожного з трьох шматків
    colors = ['#98FB98', '#87CEFA', '#FFD700']
    node_colors = {}
    node_chunks = {}

    for chunk_idx, chunk in enumerate(chunks):
        for node in chunk:
            node_colors[node] = colors[chunk_idx]
            node_chunks[node] = chunk_idx

    internal_edges = []
    cut_edges = []
    for u, v in G.edges():
        if node_chunks[u] == node_chunks[v]:
            internal_edges.append((u, v))
        else:
            cut_edges.append((u, v))

    print(f"Кількість ребер, що потрапили в розріз: {len(cut_edges)}")

    plt.figure(figsize=(11, 8))
    plt.title("Візуалізація розрізу графа на шматки (Варіант №4)", fontsize=14, fontweight='bold')

    pos = nx.spring_layout(G, seed=42, k=0.6)

    nx.draw_networkx_edges(G, pos, edgelist=internal_edges, width=1.5, edge_color='#B0B0B0')
    
    nx.draw_networkx_edges(G, pos, edgelist=cut_edges, width=2, edge_color='#FF4500', style='dashed')

    normal_nodes = [node for node in G.nodes() if node not in forbidden_vertices]
    nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, 
                           node_color=[node_colors[n] for n in normal_nodes], 
                           node_shape='o', node_size=600, edgecolors='black')

    nx.draw_networkx_nodes(G, pos, nodelist=forbidden_vertices, 
                           node_color=[node_colors[n] for n in forbidden_vertices], 
                           node_shape='s', node_size=750, edgecolors='#FF0000', linewidths=2)

    # Номери вершин
    nx.draw_networkx_labels(G, pos, font_size=11, font_weight='bold')

    legend_elements = [
        Patch(facecolor=colors[0], edgecolor='black', label=f'Шматок G1: {sorted(chunks[0])}'),
        Patch(facecolor=colors[1], edgecolor='black', label=f'Шматок G2: {sorted(chunks[1])}'),
        Patch(facecolor=colors[2], edgecolor='black', label=f'Шматок G3: {sorted(chunks[2])}'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='white', markeredgecolor='red', markersize=10, label='Заборонені вершини (Якорі)'),
        plt.Line2D([0], [0], color='#FF4500', linestyle='--', linewidth=2, label=f'Лінії розрізу ({len(cut_edges)} ребер)')
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    partition_and_visualize()