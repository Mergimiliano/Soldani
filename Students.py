from flask import Flask, request, jsonify
import yaml

app = Flask(__name__)

students = {} 

# load valid courses from config file
subjects = []
with open('students-config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)
    for course in config['courses']:
        subjects.append(course.lower())

@app.route('/students',methods=['POST'])
def add_student():
    courses = {}
    body = request.json
    id = body['id']
    # if id already in use, return error
    if id in students:
        return jsonify({'error':True})
    # add student
    surname = body['surname']
    name = body['name']
    for subject in subjects:
        courses[subject] = []
    students[id] = {
        'surname': surname,
        'name': name,
        'courses': courses
    }
    # build & send reply
    path = '/students/'+id
    return jsonify({
        'path': path,
        'id': id,
        'surname': students[id]['surname'],
        'name': students[id]['name'],
        'courses': students[id]['courses'],
    })

@app.route('/students/<id>',methods=['GET'])
def get_student(id):
    # if id not used, return error
    if id not in students:
        return jsonify({'error':True})
    # build & send reply
    return jsonify({
        'id': id,
        'surname': students[id]['surname'],
        'name': students[id]['name'],
        'courses': students[id]['courses'],
    })

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    if id not in students:
        return jsonify({'error': "Student not found"}), 404

    course = request.args.get('course')
    if not course or course.lower() not in subjects:
        return jsonify({'error': "Invalid or missing course"}), 400

    try:
        grade = int(request.args.get('grade', -1))
    except ValueError:
        return jsonify({'error': "Grade must be an integer"}), 400
    if grade < 1 or grade > 10:
        return jsonify({'error': "Missing or not valid grade"}), 400

    course = course.lower()
    if course not in students[id]['courses']:
        students[id]['courses'][course] = []
    students[id]['courses'][course].append(grade)

    return jsonify({
        'id': id,
        'surname': students[id]['surname'],
        'name': students[id]['name'],
        'courses': students[id]['courses'],
    }), 200

@app.route('/students/<id>',methods=['DELETE'])
def delete_student(id):
    # if id not used, return error
    if id not in students:
        return jsonify({'error':True})
    # delete student
    students.pop(id)
    return jsonify({})

if __name__ == '__main__':
    app.run(port=50005)