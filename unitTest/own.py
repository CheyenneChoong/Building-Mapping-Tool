import timeit

def navigate(connections:dict, start, end):
    table = {}
    keys = list(connections.keys())
    for key in keys:
        if key == start:
            table[key] = [0, ""]
        else:
            table[key] = [9999, ""]
    
    previous = start
    node = ""
    distance = 0
    temp = 0
    current = 0
    while True:
        if previous in connections.keys() and not connections[previous][0]:
            del connections[previous]
            if connections.keys():
                check = 9999
                for key in keys:
                    if table[key][0] < check and table[key][0] != 0 and key in connections.keys():
                        check = table[key][0]
                        nextKey = key
                if previous == nextKey:
                    break
                else:
                    previous = nextKey
            else:
                break
            continue
        connectedNodes:list = connections[previous][0]
        connectedDistance:list = connections[previous][1]
        node = connectedNodes[0]            
        distance = connectedDistance[0]
        
        temp = table[node][0]
        current = table[previous][0] + distance
        if current < temp:
            table[node][0] = current
            table[node][1] = previous
        del connections[previous][0][0]
        del connections[previous][1][0]

    tablePrevious = []
    tableDistance = []
    for key in keys:
        tablePrevious.append(table[key][1])
        tableDistance.append(table[key][0])

    finalPath = [end]
    finalDistance = 0
    currentNode = end
    while True:
        if currentNode in keys:
            index = keys.index(currentNode)
            currentNode = tablePrevious[index]
            finalPath.append(currentNode)
            finalDistance = finalDistance + tableDistance[index]
            if currentNode == start:
                break
        else:
            return []
    finalPath.reverse()
    return [finalPath, finalDistance]

# x = {
#     "A": [["B", "F", "D"], [2, 3, 5]],
#     "B": [["E", "A", "F", "C"], [1, 2, 4, 7]],
#     "C": [["E", "G", "B"], [3, 4, 7]],
#     "D": [["G", "E", "A"], [1, 1, 5]],
#     "E": [["B", "D", "G", "C"], [1, 1, 3, 3]],
#     "F": [["A", "B"], [3, 4]],
#     "G": [["D", "E", "C"], [1, 3, 4]],
#     "H": [["I"], [5]],
#     "I": [["H"], [5]]
# }
# y = {
#     "A": [["B", "F", "D"], [2, 3, 5]],
#     "B": [["E", "A", "F", "C"], [1, 2, 4, 7]],
#     "C": [["E", "G", "B"], [3, 4, 7]],
#     "D": [["G", "E", "A"], [1, 1, 5]],
#     "E": [["B", "D", "G", "C"], [1, 1, 3, 3]],
#     "F": [["A", "B"], [3, 4]],
#     "G": [["D", "E", "C"], [1, 3, 4]],
#     "H": [["I"], [5]],
#     "I": [["H"], [5]]
# }

y = {
    'Living Room': [['S1L'], [5]], 
    'Kitchen': [['S1R'], [5]], 
    'S1R': [[], []], 
    'S1L': [[], []]
}
start = "S1R"
end = "Kitchen"
# elapsed = timeit.timeit(lambda: navigate(x, start, end), number=1)
# print(f"{elapsed:.20f}")
result = navigate(y, start, end)
if result:
    print(result[0])
    print(result[1])