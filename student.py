from flask import request, Flask, jsonify
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
basic_auth = BasicAuth(app)

students = [
    {"std_id": 1, "name": "Student 1"},
    {"std_id": 2, "name": "Student 2"},
    {"std_id": 3, "name": "Student 3"}
]

@app.route("/")
def greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/students", methods=["GET"])
@basic_auth.required
def get_all_students():
    return jsonify({"students": students})

@app.route("/students/<int:std_id>", methods=["GET"])
@basic_auth.required
def get_student(std_id):
    student = next((s for s in students if s["std_id"] == std_id), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students", methods=["POST"])
@basic_auth.required
def create_student():
    data = request.get_json()
    existing_student = next((s for s in students if s["std_id"] == data["std_id"]), None)
    if existing_student:
        return jsonify({"error": "Cannot create new student"}), 500
    else:
        new_student = {
            "std_id": data["std_id"],
            "name": data["name"]
        }
        students.append(new_student)
        return jsonify(new_student), 201

@app.route("/students/<int:std_id>", methods=["PUT"])
@basic_auth.required
def update_student(std_id):
    student = next((s for s in students if s["std_id"] == std_id), None)
    if student:
        data = request.get_json()
        student["name"] = data.get("name", student["name"])
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<int:std_id>", methods=["DELETE"])
@basic_auth.required
def delete_student(std_id):
    student = next((s for s in students if s["std_id"] == std_id), None)
    if student:
        students.remove(student)
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
