from process.load import loadData
from process.export import Export

class Route():
    def __init__(self):
        self.__path = ""
        self.__convert = Export()
    
    def setPath(self, path:str):
        self.__path = path

    def displayOption(self) -> str:
        __data = loadData(self.__path)
        __floorList:list = __data["floors"]
        __optionList:list = __data["names"]
        __optionList = list(set(__optionList) - set(__floorList))

        __display = ""
        for __option in __optionList:
            __display = f'''
            {__display}
            <option value='{__option}'>{__option}</option>
            '''
        return __display
    
    def navigate(self, start:str, end:str) -> list:
        __startFloor = self.__identifyFloor(start)
        __endFloor = self.__identifyFloor(end)
        __roomTable:dict[str, dict[str, list[list]]] = self.__convert.roomTable(self.__path)

        __startPoint:list[list] = [[], []]
        __endPoint:list[list] = [[], []]
        if start in __roomTable[__startFloor].keys() and not start in self.__convert.floorTable(self.__path)[__startFloor]:
            __startPoint = __roomTable[__startFloor][start]
        else:
            __startPoint = [[start], [0]]
        if end in __roomTable[__endFloor].keys() and not end in self.__convert.floorTable(self.__path)[__endFloor]:
            __endPoint = __roomTable[__endFloor][end]
        else:
            __endPoint = [[end], [0]]
        
        __path = []
        __distance = 999999
        __crossFloorPath:list[list] = self.__crossFloor(__startFloor, __endFloor)
        __tempDistance = 0

        if __startFloor == __endFloor:
            for __startIndex, __point1 in enumerate(__startPoint[0]):
                for __endIndex, __point2 in enumerate(__endPoint[0]):
                    __data = self.__convert.floorTable(self.__path)[__startFloor]
                    __result = self.__dijkstra(__point1, __point2, __data)
                    if __result:
                        __tempPath = [start] + __result[0] + [end]
                        __tempDistance = __startPoint[1][__startIndex] + __result[1] + __endPoint[1][__endIndex]
                    elif __point1 == __point2:
                        __tempPath = [start] + [__point1] + [end]
                    else:
                        continue
                    if __tempDistance < __distance:
                        __path = __tempPath
                        __distance = __tempDistance
                    __tempDistance = 0
            return __path

        for __index, __crossRoute in enumerate(__crossFloorPath[2]):
            if __crossRoute[0] != __startFloor or __crossRoute[1] != __endFloor:
                continue
            for __startIndex, __point1 in enumerate(__startPoint[0]):
                for __endIndex, __point2 in enumerate(__endPoint[0]):
                    if __point1 == __crossFloorPath[0][__index][0] and __point2 == __crossFloorPath[0][__index][1]:
                        __path = [start] + [__startPoint[0][__startIndex]] + [__endPoint[0][__endIndex]] + [end]
                        return __path
                    
                    if __point1 != __crossFloorPath[0][__index][0]:
                        __data = self.__convert.floorTable(self.__path)[__startFloor]
                        __result = self.__dijkstra(__point1, __crossFloorPath[0][__index][0], __data)
                        if not __result:
                            continue
                        __toCheckpoint = [start] + __result[0]
                        __tempDistance = __tempDistance + __result[1] + __startPoint[1][__startIndex]
                    else:
                        __toCheckpoint = [start] + [__point1]
                        __tempDistance = __tempDistance + 0
                    
                    if __point2 != __crossFloorPath[0][__index][1]:
                        __data = self.__convert.floorTable(self.__path)[__endFloor]
                        __result = self.__dijkstra(__crossFloorPath[0][__index][1], __point2, __data)
                        if not __result:
                            continue
                        __fromCheckpoint = __result[0] + [end]
                        __tempDistance = __tempDistance + __result[1] + __endPoint[1][__endIndex]
                    else:
                        __fromCheckpoint = [__point2] + [end]
                        __tempDistance = __tempDistance + 0
                    
                    __tempPath = __toCheckpoint + __fromCheckpoint
                    __tempDistance = __tempDistance + __crossFloorPath[1][__index]
                    if __tempDistance < __distance:
                        __path = __tempPath
                        __distance = __tempDistance
                    __tempDistance = 0
        
        if __path:
            return __path
        else:
            return self.__dijkstra(start, end, self.__convert.allConnection(self.__path))

    def __identifyFloor(self, point:str) -> str:
        __data = loadData(self.__path)
        __floorList:list = __data["floors"]
        for __floor in __floorList:
            __roomList = __data[__floor]["room"]
            __connectorList = __data[__floor]["connector"]
            __checkpointList = __data[__floor]["checkpoint"]
            if point in __roomList or point in __connectorList or point in __checkpointList:
                return __floor
            
    def __crossFloor(self, floorStart:str, floorEnd:str) -> list:
        __data = loadData(self.__path)
        __floorList:list = __data["floors"]
        __indexStart = __floorList.index(floorStart)
        __indexEnd = __floorList.index(floorEnd)
        if __indexStart < __indexEnd:
            __floorList = __floorList[__indexStart:__indexEnd+1]
        else:
            __floorList = __floorList[__indexEnd:__indexStart+1]
            __floorList.reverse()
        
        __connectorList = __data[floorStart]["connector"]
        __crossFloorPath = [[], [], []]
        __connectionList:list[list] = __data["connect"]
        for __connector in __connectorList:
            __current = __connector
            __floor = floorStart
            __path = [__connector, ""]
            __floorJump = [floorStart, ""]
            __distance = 0
            for __floor in __floorList:
                if __floor == floorStart:
                    continue
                if __current in __connectionList[1]:
                    __indexList = [__index for __index, __check in enumerate(__connectionList[1]) if __check == __current]
                    for __index in __indexList:
                        if __connectionList[2][__index] == __floor:
                            __current = __connectionList[3][__index]
                            __distance = __distance + __connectionList[4][__index]
                            __path[1] = __current
                            __floorJump[1] = __floor
                            break
                else:
                    break
            __crossFloorPath[0].append(__path)
            __crossFloorPath[1].append(__distance)
            __crossFloorPath[2].append(__floorJump)
        return __crossFloorPath

    def __dijkstra(self, start:str, end:str, connection:dict) -> list:
        __data = connection
        __table = {}
        __keys = list(__data.keys())
        for __key in __keys:
            if __key == start:
                __table[__key] = [0, ""]
            else:
                __table[__key] = [9999, ""]

        __previous = start
        __node = ""
        __nextKey = ""
        __distance = 0
        __temp = 0
        __current = 0

        while True:
            if __previous in __data.keys() and not __data[__previous][0]:
                del __data[__previous]
                if __data.keys():
                    __check = 9999
                    for __key in __keys:
                        if __table[__key][0] < __check and __table[__key][0] != 0 and __key in __data.keys():
                            __check = __table[__key][0]
                            __nextKey = __key
                    if __previous == __nextKey:
                        break
                    elif __nextKey:
                        __previous = __nextKey
                    else:
                        break
                else:
                    break
                continue
            __connectedNodes:list = __data[__previous][0]
            __connectedDistance:list = __data[__previous][1]
            __node = __connectedNodes[0]
            __distance = __connectedDistance[0]

            __temp  = __table[__node][0]
            __current = __table[__previous][0] + __distance
            if __current < __temp:
                __table[__node][0] = __current
                __table[__node][1] = __previous
            del __data[__previous][0][0]
            del __data[__previous][1][0]

        __tablePrevious = []
        __tableDistance = []
        for __key in __keys:
            __tablePrevious.append(__table[__key][1])
            __tableDistance.append(__table[__key][0])
        
        __finalPath = [end]
        __finalDistance = 0
        __currentNode = end
        while True:
            if __currentNode in __keys:
                __index = __keys.index(__currentNode)
                __currentNode = __tablePrevious[__index]
                __finalPath.append(__currentNode)
                __finalDistance = __finalDistance + __tableDistance[__index]
                if __currentNode == start:
                    break
            else:
                return []
        __finalPath.reverse()
        return [__finalPath, __finalDistance]