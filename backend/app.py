from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    data = db.get_all_students()
    return jsonify(data), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    student_data = request.json
    if not student_data or "name" not in student_data or "course" not in student_data or "mark" not in student_data:
        return jsonify({"error": "Missing required fields"}), 404
    if not (0 <= student_data["mark"] <= 100):
        return jsonify({"error": "Mark must be between 0 and 100"}), 404

    new_student = db.insert_student(student_data["name"], student_data["course"], student_data.get("mark", 0))

    return jsonify(new_student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    updated_data = request.json

    if not updated_data or "name" not in updated_data or "course" not in updated_data or "mark" not in updated_data:
        return jsonify({"error": "Missing required fields"}), 404
    if not (0 <= updated_data["mark"] <= 100):
        return jsonify({"error": "Mark must be between 0 and 100"}), 404

    updated_student = db.update_student(student_id, updated_data["name"], updated_data["course"], updated_data["mark"])
    if updated_student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(updated_student), 200



@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student_data = db.get_student_by_id(student_id)
    if student_data is None:
        return jsonify({"error": "Student not found"}), 404
    db.delete_student(student_id)
    return jsonify(student_data), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """

    students = db.get_all_students()
    if not students:
        return jsonify({"error": "No students found"}), 404

    marks = [student["mark"] for student in students]
    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
