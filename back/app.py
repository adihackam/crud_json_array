import json
import os 
from flask import Flask, request ,redirect, render_template, url_for
from flask_cors import CORS

app = Flask(__name__, template_folder='../front')
CORS(app)

myFile= "./back/students.json"
students={}

def loadFromFile():
    isExist = os.path.exists(myFile)
    if isExist:
        with open(myFile, 'r') as openFile:
            students = json.load(openFile)
        return students
    return []

def save2File(students):
    jsonString = json.dumps(students, indent=4)
    with open(myFile, "w") as outfile:
	    outfile.write(jsonString)


@app.route('/students/', methods = ['GET', 'POST','DELETE'])
@app.route('/students/<id>', methods = ['GET', 'POST','DELETE','PUT'])
def crude_students(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        name= request_data["name"]
        age = request_data["age"]
        city = request_data['city']
        students = loadFromFile() 
        maxId = 0
        for stu in students:
            if stu['id'] > maxId : 
                maxId = stu['id']
        newStudent = {"id":maxId + 1, "name": name, "age": age, "city": city}
        students.append(newStudent)
        save2File(students)
        return {"msg":"new student was added"} 

    if request.method == 'GET':
        res=[]
        students = loadFromFile() 
        for student in students:
            res.append({"city":student['city'],"id":student['id'],"name":student['name'], "age":student['age']})
        return  res
        # return  (json.dumps(res))
    if request.method == 'DELETE': 
        students = loadFromFile() 
        for stu in students:
            if stu['id'] == int(id): 
                students.remove(stu)
        save2File(students)
        return {"msg":"row deleted"}

    if request.method == 'PUT':
        request_data = request.get_json()
        students = loadFromFile() 
        for stu in students:
            if stu['id'] == int(id): 
                stu['city'] = request_data['city']
                stu['age'] = request_data['age']
                stu['name']= request_data['name']
        save2File(students)
        return {"msg":"student updated"}

@app.route('/')
def index():
    return render_template('index.html')
 
if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug = False)