import json

def loadData(path) -> dict:
    with open(path, "r") as file:
        data = json.load(file)
    return data

def writeData(path, data:dict):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)