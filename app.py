from flask import Flask, render_template, request, redirect, url_for, Response
from process.project import Project
from process.floor import Floor
from pathlib import Path

projectEditor = Project()
floorEditor = Floor()

# Variables used in Floor Page
projectTitle = "Untitled Project"
newFloorError = ""
connectFloorError = ""
floorSearchResult = ""

# Variables used in Point Page
floorSelection = ""
addPointError = ""
connectPointError = ""

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
    return render_template(
        'floor.html', 
        projectList = projectList(), 
        projectTitle=projectTitle, 
        newFloorError=newFloorError,
        connectFloorError=connectFloorError,
        floorSearchResult=floorSearchResult,
        floorContent=floorEditor.displayFloor())

@app.route('/point')
def point():
    global floorSelection, addPointError, connectPointError
    return render_template(
        'point.html', 
        projectList = projectList(), 
        projectTitle=projectTitle,
        floorSelection=floorSelection,
        addPointError=addPointError,
        connectPointError=connectPointError)

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

if __name__ == '__main__':
    app.run(debug=True)