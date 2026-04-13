from process.load import loadData

class Export():
    def allConnection(self, path) -> dict:
        __data = loadData(path)
        __nameList = __data["names"]
        __floorList = __data["floors"]
        __pointList = list(set(__nameList) - set(__floorList))
        __pointConnectList:dict[str, list[list]] = {}
        for __point in __pointList:
            __pointConnectList[__point] = [[], []]
        
        __floorConnectList:list[list] = __data["connect"]
        __connectionList = [[], [], []]
        __connectionList[0] = __floorConnectList[1]
        __connectionList[1] = __floorConnectList[3]
        __connectionList[2] = __floorConnectList[4]
        for __floor in __floorList:
            __temp:list[list] = __data[__floor]["connect"]
            __connectionList[0] = __connectionList[0] + __temp[0] + __temp[1]
            __connectionList[1] = __connectionList[1] + __temp[1] + __temp[0]
            __connectionList[2] = __connectionList[2] + __temp[2] + __temp[2]
        
        for __index, __point in enumerate(__connectionList[0]):
            __pointConnectList[__point][0].append(__connectionList[1][__index])
            __pointConnectList[__point][1].append(__connectionList[2][__index])
        
        return __pointConnectList

    def crossFloorTable(self, path) -> dict:
        __data = loadData(path)
        __floorList = __data["floors"]
        __connectorList:dict[str, list[list]] = {}
        for __floor in __floorList:
            __tempList = __data[__floor]["connector"]
            for __connector in __tempList:
                __connectorList[__connector] = [[], []]
        
        __connectorConnection:list[list] = __data["connect"]
        for __index, __point in enumerate(__connectorConnection[1]):
            __connectorList[__point][0].append(__connectorConnection[1][__index])
            __connectorList[__point][1].append(__connectorConnection[2][__index])
        
        return __connectorList
    
    def floorTable(self, path) -> dict:
        __data = loadData(path)
        __floorList = __data["floors"]
        __connectionTable:dict[str, dict[str, list[list]]] = {}
        for __floor in __floorList:
            __connectionTable[__floor] = {}
            __connectorList = __data[__floor]["connector"]
            __checkpointList = __data[__floor]["checkpoint"]
            __pointList = list(set(__checkpointList) | set(__connectorList))
            for __point in __pointList:
                __connectionTable[__floor][__point] = [[], []]
            
            __connection:list[list] = __data[__floor]["connect"]
            __connections = __connection.copy()
            __connections[0] = __connections[0] + __connection[1]
            __connections[1] = __connections[1] + __connection[0]
            __connections[2] = __connections[2] + __connection[2]
            for __index, __point in (enumerate(__connections[0])):
                if __point in __connectionTable[__floor].keys():
                    if __connections[1][__index] in __connectionTable[__floor].keys():
                        __connectionTable[__floor][__point][0].append(__connections[1][__index])
                        __connectionTable[__floor][__point][1].append(__connections[2][__index])
        
        return __connectionTable

    def roomTable(self, path) -> dict:
        __data = loadData(path)
        __floorList = __data["floors"]
        __connectionTable:dict[str, dict[str, list[list]]] = {}
        for __floor in __floorList:
            __connectionTable[__floor] = {}
            __roomList = __data[__floor]["room"]
            __connectorList = __data[__floor]["connector"]
            __checkpointList = __data[__floor]["checkpoint"]
            __pointList = __roomList + list(set(__checkpointList) | set(__connectorList))
            for __point in __pointList:
                __connectionTable[__floor][__point] = [[], []]
            
            __connection:list[list] = __data[__floor]["connect"]
            __connections = __connection.copy()
            __connections[0] = __connections[0] + __connection[1]
            __connections[1] = __connections[1] + __connection[0]
            __connections[2] = __connections[2] + __connection[2]
            for __index, __point in (enumerate(__connections[0])):
                __connectionTable[__floor][__point][0].append(__connections[1][__index])
                __connectionTable[__floor][__point][1].append(__connections[2][__index])
        return __connectionTable
    
    def downloadData(self, path) -> dict:
        __file = loadData(path)
        __data = {
            "floors": __file["floors"],
            "points": __file["names"],
        }
        __floorList = __file["floors"]
        for __floor in __floorList:
            __data[__floor] = __file[__floor]["room"] + list(set(__file[__floor]["checkpoint"]) | set(__file[__floor]["connector"]))
        __data["all"] = self.allConnection(path)
        __data["room-checkpoint"] = self.roomTable(path)
        __data["checkpoint-checkpoint"] = self.floorTable(path)
        __data["floor-floor"] = self.crossFloorTable(path)
        return __data

    def sql(self, path, table, column):
        __data = loadData(path)
        __nameList = __data["names"]
        __floorList = __data["floors"]
        __dataList = list(set(__nameList) - set(__floorList))

        __generatedString = ""
        for __name in __dataList:
            __generatedString = f"{__generatedString}INSERT INTO {table} ({column}) VALUES ('{__name}');<br/>"
        return __generatedString