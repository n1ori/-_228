graph = {
    1: {2: 3, 3: 5, 4: 4},
    2: {5: 2, 6: 2},
    3: {6: 3, 7: 3},
    4: {6: 2, 7: 2},
    5: {8: 2, 9: 1, 10: 1},
    6: {8: 2, 10: 2},
    7: {10: 3, 11: 2},
    8: {12: 3},
    9: {12: 2},
    10: {11: 1, 12: 2, 13: 1},
    11: {13: 2},
    12: {14: 7},
    13: {14: 5},
    14: {}
}

def wave_algorithm():
    distances = {node: float('inf') for node in graph}
    distances[1] = 0
    M = [1]
    
    while M:
        u = M.pop(0)
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                if v not in M:
                    M.append(v)
    
    print(f"Відстань до x14 (Хвильовий): {distances[14]}")

wave_algorithm()