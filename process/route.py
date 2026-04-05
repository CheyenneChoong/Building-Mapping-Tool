from process.load import loadData

class Route():
    def __init__(self):
        self.__path = ""
    
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
            <option value='{__display}'>{__display}</option>
            '''
        return __display
    
    def __identifyPoint(self, point) -> dict:
        __data = loadData(self.__path)
        __floorList:list = __data["floors"]
        __pointIdentity = []
        __status = 0

        for __floor in __floorList:
            __currentFloor:dict = __data[__floor]
            for __type in ["room", "connector", "checkpoint"]:
                if point in __currentFloor[__type]:
                    __pointIdentity = {
                        "name": point,
                        "floor": __floor,
                        "type": __type
                    }
                    __status = 1
                    break
            if __status == 1:
                break

        return __pointIdentity
    
    def __connectedCheckpoint(self, point) -> list:
        __data = loadData(self.__path)
        __pointInfo = self.__identifyPoint(point)
        __floorInfo:dict = __data[__pointInfo["floor"]]
        __connectList:list = __floorInfo["connect"]
        
        __connection1:list = [__index for __index, __check in enumerate(__connectList[0]) if __check == point]
        __connection2:list = [__index for __index, __check in enumerate(__connectList[1]) if __check == point]
        __connectionList = list(set(__connection1 | __connection2))

        __checkpoint = [[], []]
        for __connection in __connectionList:
            __check:dict = self.__identifyPoint(__connectionList[1][__connection])
            if __check["type"] != "room":
                __checkpoint[0].append(__connectionList[1][__connection])
                __checkpoint[1].append(__connectionList[2][__connection])
        return __checkpoint

    def __navigateCheckpoint(self, point1, point2) -> list:
        __visited = []
        __edges = []
        __shortcut = []
        __current = point1
        while True:
            __next:list[list] = self.__connectedCheckpoint(__current)
            if point2 in __next[0]:
                __index = __next.index(point2)