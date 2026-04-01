from process.load import loadData, writeData

class Point():
    def __init__(self):
        self.__path = ""
    
    def setPath(self, path:str):
        self.__path = path

    def displayDetails(self, floor:str) -> str:
        if not floor:
            return ""
        
        __data = loadData(self.__path)
        __floorDetail:dict = __data[floor]
        __roomList:list = __floorDetail["room"]
        __roomDisplay = ""
        for __room in __roomList:
            __roomDisplay = f'''
            {__roomDisplay}
            <button id="{__room}" class="displayButton" onclick="point.highlight('{__room}')">{__room}</button>
            '''
        
        __connectorList:list = __floorDetail["connector"]
        __connectorDisplay = ""
        for __connector in __connectorList:
            __connectorDisplay = f'''
            {__connectorDisplay}
            <button id="{__connector}" class="displayButton" onclick="point.highlight('{__connector}')" >{__connector}</button>
            '''
        
        __checkpointList:list = __floorDetail["checkpoint"]
        __checkpointDisplay = ""
        for __checkpoint in __checkpointList:
            __checkpointDisplay = f'''
            {__checkpointDisplay}
            <button id="{__checkpoint}" class="displayButton" onclick="point.highlight('{__checkpoint}')">{__checkpoint}</button>
            '''

        __display = f'''
        <div class="displayPanel" id="display1">
            <div class="titlePanel">
                <strong>Rooms</strong>
            </div>
            <div class="floorContent" id="roomDisplay">
                {__roomDisplay}
            </div>
        </div>
        <div class="displayPanel" id="display2">
            <div class="titlePanel">
                <strong>Connectors</strong>
            </div>
            <div class="floorContent" id="connectorDisplay">
                {__connectorDisplay}
            </div>
        </div>
        <div class="displayPanel" id="display3">
            <div class="titlePanel">
                <strong>Checkpoints</strong>
            </div>
            <div class="floorContent" id="checkpointDisplay">
                {__checkpointDisplay}
            </div>
        </div>
        '''
        return __display

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
            __floorConnect:list[list] = __data["connect"]
            __deleteList1:list = [__index for __index, __check in enumerate(__floorConnect[1]) if __check == name]
            __deleteList2:list = [__index for __index, __check in enumerate(__floorConnect[3]) if __check == name]
            __deleteList = list(set(__deleteList1) | set(__deleteList2))
            __deleteList.sort(reverse=True)
            for __delete in __deleteList:
                del __floorConnect[0][__delete]
                del __floorConnect[1][__delete]
                del __floorConnect[2][__delete]
                del __floorConnect[3][__delete]
                del __floorConnect[4][__delete]
            __data["connect"] = __floorConnect
        if name in __checkpointList:
            __checkpointList.remove(name)
        
        __connectList:list[list] = __floorInfo["connect"]
        __deleteList1 = [__index for __index, __check in enumerate(__connectList[0]) if __check == name]
        __deleteList2 = [__index for __index, __check in enumerate(__connectList[1]) if __check == name]
        __deleteList = list(set(__deleteList1) | set(__deleteList2))
        __deleteList.sort(reverse=True)
        for __delete in __deleteList:
            del __connectList[0][__delete]
            del __connectList[1][__delete]
            del __connectList[2][__delete]
        __floorInfo["connect"] = __connectList

        __floorInfo["room"] = __roomList
        __floorInfo["connector"] = __connectorList
        __floorInfo["checkpoint"] = __checkpointList
        __data[floor] = __floorInfo
        __data["names"] = __nameList
        writeData(self.__path, __data)
        return ""

    def checkType(self, floor:str, name:str, type:str) -> bool:
        __data = loadData(self.__path)
        __floorDetails:dict = __data[floor]
        __list:list = __floorDetails[type]
        if name in __list:
            return True
        else:
            return False
    
    def connectPoint(self, floor:str, point1:str, point2:str, distance:int) -> str:
        __data = loadData(self.__path)
        if point1 == point2:
            return "Can't map point to itself."
        __check = self.getPointConnectIndex(floor, point1, point2)

        if __check != -1:
            return "Connection exists."
        
        __floorDetail:dict = __data[floor]
        __error = ""
        for __type in ["room", "connector", "checkpoint"]:
            if point1 not in __floorDetail[__type]:
                __error = f"{point1} doesn't exists in this floor."
            else:
                __error = ""
            if point2 not in __floorDetail[__type]:
                __error = f"{point2} doesn't exists in this floor."
            else:
                __error = ""
        if __error:
            return __error

        __connections:list[list] = __floorDetail["connect"]
        __connections[0].append(point1)
        __connections[1].append(point2)
        __connections[2].append(distance)
        __floorDetail["connect"] = __connections
        __data[floor] = __floorDetail
        writeData(self.__path, __data)
        return ""

    def getPointConnectIndex(self, floor:str, point1:str, point2:str) -> int:
        __data = loadData(self.__path)
        __floorDetails:dict = __data[floor]
        __connections:list = __floorDetails["connect"]
        __searchList1:list = [__index for __index, __check in enumerate(__connections[0]) if __check == point1 or __check == point2]
        __searchList2:list = [__index for __index, __check in enumerate(__connections[1]) if __check == point1 or __check == point2]
        __index = list(set(__searchList1) & set(__searchList2))
        if __index:
            return __index[0]
        else:
            return -1
    
    def getPointConnectData(self, floor:str) -> list:
        if not floor:
            return [[], [], []]
        __data = loadData(self.__path)
        __floorDetail:dict = __data[floor]
        return __floorDetail["connect"]

    def removePointConnect(self, floor:str, point1:str, point2:str) -> str:
        __index = self.getPointConnectIndex(floor, point1, point2)
        if __index == -1:
            return "Connection doesn't exists."
        __data = loadData(self.__path)
        __floorDetail:dict = __data[floor]
        __connections:list = __floorDetail["connect"]
        del __connections[0][__index]
        del __connections[1][__index]
        del __connections[2][__index]
        
        __floorDetail["connect"] = __connections
        __data[floor] = __floorDetail
        writeData(self.__path, __data)
        return ""