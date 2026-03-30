from process.load import loadData, writeData

class Floor():
    def __init__(self, path:str):
        self.__path = path
    
    def getFloor(self) -> list:
        __data = loadData(self.__path)
        return __data["floors"]
    
    def getConnector(self, floor:str) -> list:
        __data = loadData(self.__path)
        return __data[floor]["connector"]
    
    def checkConnector(self, floor:str, connector:str) -> bool:
        __connectorList = self.getConnector(floor)
        if connector in __connectorList:
            return True
        else:
            return False

    def changePosition(self, floor:str, position:int):
        __data = loadData(self.__path)
        __floorList:list[str] = __data["floors"]
        __index = __floorList.index(floor)
        __temp = __floorList[__index + position]
        __floorList[__index + position] = floor
        __floorList[__index] = __temp
        __data["floors"] = __floorList
        writeData(self.__path, __data)
    
    def addFloor(self, floor:str) -> str:
        __data = loadData(self.__path)
        __nameList:list[str] = __data["names"]
        __floorList:list[str] = __data["floors"]

        if floor in __nameList:
            return "Floor already exists."
        __nameList.append(floor)
        __floorList.append(floor)
        __data["names"] = __nameList
        __data["floors"] = __floorList
        __data[floor] = {
            "room": [],
            "checkpoint": [],
            "connector": [],
            "connect": [[], [], []]
        }
        writeData(self.__path, __data)
        return ""
    
    def removeFloor(self, floor:str):
        __data = loadData(self.__path)
        __nameList:list[str] = __data["names"]
        __floorList:list[str] = __data["floors"]
        __connectList:list = __data["connect"]

        __removeList1:list = [__index for __index, __check in enumerate(__connectList[0]) if __check == floor]
        __removeList2:list = [__index for __index, __check in enumerate(__connectList[1]) if __check == floor]
        __indexList:list = list(set(__removeList1 + __removeList2))

        __nameList.remove(floor)
        __floorList.remove(floor)
        for __index in __indexList:
            del __connectList[0][__index]
            del __connectList[1][__index]
            del __connectList[2][__index]
            del __connectList[3][__index]
            del __connectList[4][__index]
        __data["names"] = __nameList
        __data["floors"] = __floorList
        __data["connect"] = __connectList
        del __data[floor]

        writeData(self.__path, __data)