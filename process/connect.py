from process.load import loadData, writeData

class Connect():
    def __init__(self, path:str):
        self.__path = path
    
    def connectFloor(self, floor1:str, point1:str, floor2:str, point2:str, distance:int) -> str:
        __check:list = self.getFloorConnect(point1, point2)
        if __check:
            return "Connection already exists."

        __data = loadData(self.__path)
        __connectList:list[list] = __data["connect"]
        __connectList[0].append(floor1)
        __connectList[1].append(point1)
        __connectList[2].append(floor2)
        __connectList[3].append(point2)
        __connectList[4].append(distance)
        __data["connect"] = __connectList
        writeData(self.__path, __data)
        return ""
    
    def getFloorConnect(self, point1:str, point2:str) -> list:
        __data = loadData(self.__path)
        __connectList:list[list] = __data["connect"]
        __searchList1:list = [__index for __index, __check in enumerate(__connectList[1]) if __check == point1]
        __searchList2:list = [__index for __index, __check in enumerate(__connectList[3]) if __check == point2]
        __index = list(set(__searchList1) & set(__searchList2))

        if __index:
            __floor1 = __connectList[0][__index[0]]
            __point1 = __connectList[1][__index[0]]
            __floor2 = __connectList[2][__index[0]]
            __point2 = __connectList[3][__index[0]]
            __distance = __connectList[4][__index[0]]
            return [__floor1, __point1, __floor2, __point2, __distance]
        else:
            return []