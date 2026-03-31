from flask import Flask, render_template, request, redirect, url_for, Response
from process.project import Project
from process.floor import Floor
from process.point import Point
from pathlib import Path

projectEditor = Project()
floorEditor = Floor()
pointEditor = Point()

# Variables used in Floor Page
projectTitle = "Untitled Project"
newFloorError = ""
connectFloorError = ""
floorSearchResult = ""

# Variables used in Point Page
floorSelection = ""
addPointError = ""
connectPointError = ""
currentFloor = ""

def projectList() -> str:
    data = ""
    with open(Path("project/project.txt").absolute(), "r") as file:
        for line in file:
            data = f"""
            {data}
            {line.strip("\n")}<br />
            """
    return data

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html', projectList = projectList(), projectTitle = projectTitle)

@app.route('/floor')
def floor():
    global projectTitle, newFloorError, connectFloorError, floorSearchResult
    data = floorEditor.floorConnectData()
    return render_template(
        'floor.html', 
        projectList = projectList(), 
        projectTitle=projectTitle, 
        newFloorError=newFloorError,
        connectFloorError=connectFloorError,
        floorSearchResult=floorSearchResult,
        floorContent=floorEditor.displayFloor(),
        startConnector=data[0],
        endConnector=data[1],
        distance=data[2])

@app.route('/point', methods=["GET"])
def point():
    global currentFloor
    currentFloor = request.args.get("floor")
    return render_template(
        'point.html', 
        projectList = projectList(), 
        projectTitle=projectTitle,
        floorSelection=floorSelection,
        addPointError=addPointError,
        connectPointError=connectPointError,
        displayRoom=pointEditor.displayDetails(currentFloor),)

@app.route('/test')
def test():
    return render_template('test.html', projectList = projectList(), projectTitle=projectTitle)

@app.route('/newProject', methods=["POST"])
def newProject():
    projectName = request.form.get("fileName")
    projectEditor.newProject(projectName.strip())
    return redirect(url_for('home'))

@app.route('/openProject', methods=["POST"])
def openProject():
    global projectTitle, floorSelection

    projectName = request.form.get("fileName")
    projectEditor.openProject(projectName.strip())
    floorEditor.setPath(projectEditor.getPath())
    pointEditor.setPath(projectEditor.getPath())
    projectTitle = projectEditor.getTitle()
    floorSelection = floorEditor.selectFloor()
    return redirect(url_for('floor'))

@app.route('/newFloor', methods=["POST"])
def newFloor():
    global newFloorError
    floorName = request.form.get("floorName")
    newFloorError = floorEditor.addFloor(floorName.strip())
    return redirect(url_for('floor'))

@app.route('/repositionUp', methods=["POST"])
def repositionUp():
    floorName = request.form.get("floorName")
    floorEditor.changePosition(floorName, 1)
    return redirect(url_for('floor'))

@app.route('/repositionDown', methods=["POST"])
def repositionDown():
    floorName = request.form.get("floorName")
    floorEditor.changePosition(floorName, -1)
    return redirect(url_for('floor'))

@app.route('/deleteFloor', methods=["POST"])
def deleteFloor():
    floorName = request.form.get("floorName")
    floorEditor.removeFloor(floorName)
    return redirect(url_for('floor'))

@app.route('/connectFloor', methods=["POST"])
def connectFloor():
    global connectFloorError
    floor1 = request.form.get("floor1")
    floor2 = request.form.get("floor2")
    point1 = request.form.get("point1")
    point2 = request.form.get("point2")
    distance:int = int(request.form.get("distance"))
    if floorEditor.checkFloor(floor1) and floorEditor.checkFloor(floor2):
        if pointEditor.checkType(floor1, point1, "connector") and pointEditor.checkType(floor2, point2, "connector"):
            connectFloorError = floorEditor.connectFloor(floor1, point1, floor2, point2, distance)
        else:
            connectFloorError = "Check for typo in connector name."
    else:
        connectFloorError = "Check for typo in floor name."
    return redirect(url_for('floor'))

@app.route('/addPoint', methods=["POST"])
def addPoint():
    global addPointError
    pointName = request.form.get("name")
    type = request.form.get("type")
    check = request.form.get("checkpoint")
    floor = request.form.get("floor")
    if check.lower() == "true":
        checkpoint = True
    else:
        checkpoint = False
    if projectEditor.check(pointName):
        addPointError = "Name already taken."
    else:
        addPointError = pointEditor.addPoint(floor, pointName, type, checkpoint)
    return redirect(url_for('point', floor=floor))

@app.route('/deletePoint', methods=["POST"])
def deletePoint():
    global addPointError
    pointName = request.form.get("name")
    floor = request.form.get("floor")
    if projectEditor.check(pointName):
        addPointError = pointEditor.removePoint(floor, pointName)
    else:
        addPointError = "Point doesn't exist."
    return redirect(url_for('point', floor=floor))

if __name__ == '__main__':
    app.run(debug=True)