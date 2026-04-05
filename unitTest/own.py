# Testing of algorithm.
# Comparing dijsktra algorithm with own.
# This is my approach.

# Attempt 2
def navigate(connections:dict, start, end):
    previous = ""
    current = start

    path, visited = [start], [start]
    total, distance = [0], [0]
    displace = {}
    for key in connections.keys():
        displace[key] = 0
    check = 0
    loop = 1

    while True:
        print(f"Loop {loop}")
        print(f"Current: {current} | Previous: {previous} | Displace {displace[current]}")

        nextNodes:list[list] = connections[current]
        if previous in nextNodes[0]:
            index = nextNodes[0].index(previous)
            del connections[current][0][index]
            del connections[current][1][index]
            nextNodes = connections[current]
        print(f"Next Nodes: {nextNodes[0]}")
        
        # Checks if the neighbour is the destination. Sets the check value.
        if end in nextNodes[0] and check == 0:
            path = visited.copy()
            path.append(end)
            total = distance.copy()
            total.append(nextNodes[1][nextNodes[0].index(end)])
            check = sum(total)
            print(f"Neighbour exists. {path}, {total}, {check}")
        
        if not nextNodes[0] or displace[current] >= len(nextNodes[0]):
            displace[previous] += 1
            index = visited.index(current)
            del visited[index]
            del distance[index]
            current = previous
            previous = visited[-1]
            loop += 1
            print("")
            continue

        if nextNodes[0][displace[current]] in visited and current != end:
            index = visited.index(nextNodes[0][displace[current]])
            visited = visited[:index+1]
            visited.append(current)
            distance = distance[:index+1]
            distance.append(nextNodes[1][displace[current]])
            displace[current] += 1
            loop += 1
            print("")
            continue

        if nextNodes[0][displace[current]] in visited and current == end:
            index = visited.index(nextNodes[0][displace[current]])
            visited = visited[:index+1]
            visited.append(current)
            distance = distance[:index+1]
            distance.append(nextNodes[1][displace[current]])

        # Checks if the alternate route is longer than the direct to destination.
        if check > 0 and sum(distance) >= check:
            print(f"Break Out: Check -> {check}, Sum distance -> {sum(distance)}, Distance -> {distance}")
            break
        elif check > 0 and current == end:
            path = visited.copy()
            total = distance.copy()
            break

        visited.append(nextNodes[0][displace[current]])
        distance.append(nextNodes[1][displace[current]])
        previous = current
        current = nextNodes[0][displace[current]]

        print(f"Append to Visit: {nextNodes[0][displace[current]]}")
        print(f"Append to Distance: {nextNodes[1][displace[current]]}")
        print(f"Visited {visited}")
        print(f"Distance {distance}")
        loop += 1
        print("")

    return [path, total]


x = {
    "A": [["B", "F", "D"], [2, 3, 5]],
    "B": [["E", "A", "F", "C"], [1, 2, 4, 7]],
    "C": [["E", "G", "B"], [3, 4, 7]],
    "D": [["G", "E", "A"], [1, 1, 5]],
    "E": [["B", "D", "G", "C"], [1, 1, 3, 3]],
    "F": [["A", "B"], [3, 4]],
    "G": [["D", "E", "C"], [1, 3, 4]]
}
result = navigate(x, "C", "G")
print("\n\nResult")
print(result[0])
print(result[1])