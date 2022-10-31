import sys
from heapq import heapify, heappush, heappop

def dijkstra(graph, src, dest):
    inf = sys.maxsize
    node_data = {
        'A':{'cost':inf, 'pred':[]},
        'B':{'cost':inf, 'pred':[]},
        'C':{'cost':inf, 'pred':[]},
        'D':{'cost':inf, 'pred':[]},
        'E':{'cost':inf, 'pred':[]},
        'F':{'cost':inf, 'pred':[]},
        'G':{'cost':inf, 'pred':[]},
        'H':{'cost':inf, 'pred':[]},
        'I':{'cost':inf, 'pred':[]},
        'J':{'cost':inf, 'pred':[]},
    }
    node_data[src]['cost'] = 0
    visited = []
    temp = src
    for i in range(9):
        if temp not in visited:
            visited.append(temp)
            min_heap = []
            for j in graph[temp]:
                if j not in visited:
                    cost = node_data[temp]['cost'] + graph[temp][j]
                    if cost < node_data[j]['cost']:
                        node_data[j]['cost'] = cost
                        node_data[j]['pred'] = node_data[temp]['pred'] + list(temp)
                    heappush(min_heap, (node_data[j]['cost'], j))
        heapify(min_heap)
        temp = min_heap[0][1]
    print("Shortest Distance: " + str(node_data[dest]['cost']))
    print("Shortest Path: " + str(node_data[dest]['pred'] + list(dest)))

if __name__ == "__main__":
    graph = {
        'A':{'B':15, 'C':38, 'E':195, 'F':240, 'G':150, 'H':263, 'I':300, 'J':675},
        'B':{'A':15, 'C':45, 'E':195, 'F':240, 'G':150, 'H':263, 'I':300, 'J':675},
        'C':{'A':38, 'B':45, 'E':195, 'F':240, 'G':150, 'H':263, 'I':300, 'J':675},
        'D':{'E':135, 'F':180, 'G':95},
        'E':{'A':195, 'B':195, 'C':195, 'D':135, 'H':68, 'I':113, 'J':495},
        'F':{'A':240, 'B':240, 'C':240, 'D':180, 'H':38, 'I':68, 'J':450},
        'G':{'A':150, 'B':150, 'C':150, 'D':95},
        'H':{'A':263, 'B':263, 'C':263, 'E':68, 'F':38, 'J':444},
        'I':{'A':300, 'B':300, 'C':300, 'E':113, 'F':68},
        'J':{'A':675, 'B':675, 'C':675, 'E':495, 'F':450, 'H':444}
    }

    source = 'I'
    destination = 'G'
    dijkstra(graph, source, destination)
