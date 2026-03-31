from process.load import loadData, writeData

class Point():
    def __init__(self):
        self.__path = ""
    
    def setPath(self, path:str):
        self.__path = path

    def addPoint(self, floor:str, name:str, type:str, checkpoint:bool) -> str:
        __data = loadData(self.__path)
        __nameList:list = __data["names"]
        __floorInfo:dict = __data[floor]
        __roomList:list = __floorInfo["room"]
        __connectorList:list = __floorInfo["connector"]
        __checkpointList:list = __floorInfo["checkpoint"]
        __nameList.append(name)
        if type == "Room":
            __roomList.append(name)
        elif type == "Connector":
            __connectorList.append(name)
        if type == "Checkpoint" or checkpoint == True:
            __checkpointList.append(name)
        __data["names"] = __nameList
        __floorInfo["room"] = __roomList
        __floorInfo["connector"] = __connectorList
        __floorInfo["checkpoint"] = __checkpointList
        __data[floor] = __floorInfo
        writeData(self.__path, __data)
        return ""
    
    def removePoint(self, floor:str, name:str) -> str:
        __data = loadData(self.__path)
        __floorInfo:dict = __data[floor]
        __nameList:list = __data["names"]
        __roomList:list = __floorInfo["room"]
        __connectorList:list = __floorInfo["connector"]
        __checkpointList:list = __floorInfo["checkpoint"]

        __nameList.remove(name)
        if name in __roomList:
            __roomList.remove(name)
        elif name in __connectorList:
            __connectorList.remove(name)
        if name in __checkpointList:
            __checkpointList.remove(name)
        
        __floorInfo["room"] = __roomList
        __floorInfo["connector"] = __connectorList
        __floorInfo["checkpoint"] = __checkpointList
        __data[floor] = __floorInfo
        __data["names"] = __nameList
        writeData(self.__path, __data)
        return