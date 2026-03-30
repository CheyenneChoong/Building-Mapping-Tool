from flask import Flask, render_template, request, redirect, url_for, Response
from process.project import Project
from process.floor import Floor
from pathlib import Path

projectEditor = Project()
floorEditor = Floor()

projectTitle = "Untitled Project"
newFloorError = ""
connectFloorError = ""
floorSearchResult = ""

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
    return render_template('point.html', projectList = projectList(), projectTitle=projectTitle)

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
    global projectTitle

    projectName = request.form.get("fileName")
    projectEditor.openProject(projectName.strip())
    floorEditor.setPath(projectEditor.getPath())
    projectTitle = projectEditor.getTitle()
    return redirect(url_for('floor'))

@app.route('/newFloor', methods=["POST"])
def newFloor():
    global newFloorError
    floorName = request.form.get("floorName")
    newFloorError = floorEditor.addFloor(floorName.strip())
    return redirect(url_for('floor'))

if __name__ == '__main__':
    app.run(debug=True)