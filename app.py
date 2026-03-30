from flask import Flask, render_template, request, redirect, url_for, Response
from process.project import Project
from pathlib import Path

projectEditor = Project()

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
    return render_template('index.html', projectList = projectList(), projectTitle = "Untitled Project")

@app.route('/floor')
def floor():
    projectTitle = projectEditor.getTitle()
    return render_template('floor.html', projectList = projectList(), projectTitle=projectTitle)

@app.route('/point')
def point():
    projectTitle = projectEditor.getTitle()
    return render_template('point.html', projectList = projectList(), projectTitle=projectTitle)

@app.route('/test')
def test():
    projectTitle = projectEditor.getTitle()
    return render_template('test.html', projectList = projectList(), projectTitle=projectTitle)

@app.route('/newProject', methods=["POST"])
def newProject():
    projectName = request.form.get("fileName")
    projectEditor.newProject(projectName.strip())
    return redirect(url_for('home'))

@app.route('/openProject', methods=["POST"])
def openProject():
    projectName = request.form.get("fileName")
    projectEditor.openProject(projectName.strip())
    return redirect(url_for('floor'))

if __name__ == '__main__':
    app.run(debug=True)