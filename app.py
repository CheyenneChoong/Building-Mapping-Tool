from flask import Flask, render_template, request, redirect, url_for, Response
from process.project import Project
from pathlib import Path

projectEditor = Project()

app = Flask(__name__)
@app.route('/')
def home():
    data = ""
    with open(Path("process/project/project.txt").absolute(), "r") as file:
        for line in file:
            data = f"""
            {data}
            {line.strip("\n")}<br />
            """
    return render_template('index.html', projectList = data)

@app.route('/floor')
def floor():
    return render_template('floor.html')

@app.route('/point')
def point():
    return render_template('point.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/newProject', methods=["POST"])
def newProject():
    projectName = request.form.get("fileName")
    projectEditor.newProject(projectName.strip())
    return redirect(url_for('home'))

@app.route('/openProject', methods=["POST"])
def openProject():
    projectName = request.form.get("fileName")
    projectEditor.openProject(projectName.strip())
    print("Successfully Open")
    return redirect(url_for('floor'))

if __name__ == '__main__':
    app.run(debug=True)