import networkx as nx
import matplotlib.pyplot as plt

# 1. Ваші дані
adj = {
    1: [2, 7, 10, 11, 12, 16], 2: [1, 5, 7, 11, 12], 3: [7, 9, 11, 12, 13], 
    4: [5, 9, 14, 16], 5: [2, 4, 7, 14, 16], 6: [8, 10, 13, 15], 
    7: [1, 2, 3, 5, 9, 11, 12, 14, 15, 16], 8: [6, 12, 14, 15], 
    9: [3, 4, 7, 14, 16], 10: [1, 6, 12, 13, 15], 11: [1, 2, 3, 7, 14, 15], 
    12: [1, 2, 3, 7, 8, 10, 14, 15], 13: [3, 6, 10, 15], 
    14: [4, 5, 7, 8, 9, 11, 12, 15], 15: [6, 7, 8, 10, 11, 12, 13, 14], 
    16: [1, 4, 5, 7, 9]
}

def run_analysis():
    groups = {7: [7], 14: [14], 15: [15]}
    limits = {7: 6, 14: 5, 15: 5}
    remaining = [n for n in range(1, 17) if n not in [7, 14, 15]]
    
    print("=== АВТОМАТИЧНИЙ РОЗПОДІЛ ЗА ВАШИМ АЛГОРИТМОМ ===")
    
    while remaining:
        best_node, best_group, min_w = None, None, float('inf')
        
        for g_id, members in groups.items():
            if len(members) < limits[g_id]:
                for cand in remaining:
                    k_in = sum(1 for n in adj[cand] if n in members)
                    weight = len(adj[cand]) - k_in
                    if weight < min_w:
                        min_w, best_node, best_group = weight, cand, g_id
        
        if best_node:
            groups[best_group].append(best_node)
            remaining.remove(best_node)
            print(f"Додано вершину {best_node} до групи {best_group} (вага: {min_w})")

    # Виведення результатів для звіту
    print("\n--- ПІДСУМКОВИЙ РОЗПОДІЛ ---")
    for g, nodes in groups.items():
        print(f"Група з центром {g}: {sorted(nodes)} | Кількість: {len(nodes)}")
    
    return groups

# Запуск і візуалізація
final_groups = run_analysis()

# Візуалізація
G = nx.Graph()
for u, neighbors in adj.items():
    for v in neighbors: G.add_edge(u, v)

pos = nx.spring_layout(G, seed=10)
colors = []
for node in G.nodes():
    if node in final_groups[7]: colors.append('#90EE90')
    elif node in final_groups[14]: colors.append('#87CEEB')
    else: colors.append('#FFD700')

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_weight='bold')
plt.title("Результат програмного розбиття")
plt.show()