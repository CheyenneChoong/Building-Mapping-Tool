from process.load import loadData, writeData

class Point():
    def __init__(self):
        self.__path = ""
    
    def setPath(self, path:str):
        self.__path = path
        print("Point path set")

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
            <button id="{__room}" class="displayButton">{__room}</button>
            '''
        
        __connectorList:list = __floorDetail["connector"]
        __connectorDisplay = ""
        for __connector in __connectorList:
            __connectorDisplay = f'''
            {__connectorDisplay}
            <button id="{__connector}" class="displayButton">{__connector}</button>
            '''
        
        __checkpointList:list = __floorDetail["checkpoint"]
        __checkpointDisplay = ""
        for __checkpoint in __checkpointList:
            __checkpointDisplay = f'''
            {__checkpointDisplay}
            <button id="{__checkpoint}" class="displayButton">{__checkpoint}</button>
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
        if name in __checkpointList:
            __checkpointList.remove(name)
        
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