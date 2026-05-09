import heapq
 
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

def dijkstra_algorithm():
    distances = {node: float('inf') for node in graph}
    distances[1] = 0
    
    priority_queue = [(0, 1)]
    
    print("--- Процес розрахунку алгоритмом Дейкстри ---")
    
    while priority_queue:
        current_distance, u = heapq.heappop(priority_queue)
        
        if current_distance > distances[u]:
            continue
            
        for v, weight in graph[u].items():
            distance = current_distance + weight
            
            if distance < distances[v]:
                distances[v] = distance
                heapq.heappush(priority_queue, (distance, v))
                print(f"Оновлено x{v}: нова відстань {distance} (через x{u})")

    print("\n--- Результат ---")
    print(f"Мінімальна відстань до x14: {distances[14]}")

dijkstra_algorithm()