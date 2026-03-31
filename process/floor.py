from process.load import loadData, writeData

class Floor():
    def __init__(self):
        self.__path = ""

    def setPath(self, path:str):
        self.__path = path

    def displayFloor(self) -> str:
        __floorList:list = self.getFloor()
        __floorList = __floorList[::-1]
        __display:str = ""
        for __floor in __floorList:
            __connectorList:list = self.getConnector(__floor)
            __content:str = ""
            for __connector in __connectorList:
                __content = f'''
                {__content}
                <button type="button" id="{__connector}" class="displayButton">{__connector}</button>
                '''
            __display = f'''
            {__display}
            <div class="displayPanel">
                <div class="titlePanel">
                    <strong>{__floor}</strong>
                    <form method="post">
                        <input type="hidden" name="floorName" value="{__floor}" />
                        <button type="submit" formaction="/repositionUp">Up</button>
                        <button type="submit" formaction="/repositionDown">Down</button>
                        <button type="submit" formaction="/deleteFloor">Delete</button>
                    </form>
                </div>
                <div class="floorContent">
                    {__content}
                </div>
            </div>
            '''
        return __display

    def selectFloor(self) -> str:
        __floorList = self.getFloor()
        __display = "<option value="">--Select Floor--</option>"
        for __floor in __floorList:
            __display = f'''
            {__display}
            <option value="{__floor}" id="{__floor}">{__floor}</option>
            '''
        return __display

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
        if __index == (len(__floorList) - 1):
            __index = -1
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