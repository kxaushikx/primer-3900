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
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception:
        return jsonify({"error": "Failed to fetch students"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    try:
        student_data = request.json
        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark", 0)

        normalized_name = name.strip().lower()
        normalized_course = course.strip().lower()

        existing_students = db.get_all_students()
        for student in existing_students:
            if (
                student["name"].strip().lower() == normalized_name
                and student["course"].strip().lower() == normalized_course
            ):
                return jsonify({"error": "Student already exists in this course"}), 404

        student = db.insert_student(name, course, mark)
        return jsonify(student), 200
    except Exception:
        return jsonify({"error": "Failed to create student"}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        student_data = request.json
        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")

        existing_student = db.get_student_by_id(student_id)
        if existing_student is None:
            return jsonify({"error": "Student ID does not exist"}), 404

        candidate_name = name if name is not None and name != "" else existing_student["name"]
        candidate_course = course if course is not None and course != "" else existing_student["course"]

        normalized_name = candidate_name.strip().lower()
        normalized_course = candidate_course.strip().lower()

        existing_students = db.get_all_students()
        for student in existing_students:
            if student["id"] == student_id:
                continue

            if (
                student["name"].strip().lower() == normalized_name
                and student["course"].strip().lower() == normalized_course
            ):
                return jsonify({"error": "Student already exists in this course"}), 404

        student = db.update_student(student_id, name, course, mark)

        if student is None:
            return jsonify({"error": "Student ID does not exist"}), 404

        return jsonify(student), 200
    except Exception:
        return jsonify({"error": "Failed to update student"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        student = db.delete_student(student_id)

        if student is None:
            return jsonify({"error": "Student ID does not exist"}), 404

        return jsonify(student), 200
    except Exception:
        return jsonify({"error": "Failed to delete student"}), 404



@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        marks = [student["mark"] for student in students]

        if not marks:
            stats = {
                "count": 0,
                "average": 0,
                "min": 0,
                "max": 0,
            }
        else:
            stats = {
                "count": len(marks),
                "average": sum(marks) / len(marks),
                "min": min(marks),
                "max": max(marks),
            }

        return jsonify(stats), 200
    except Exception:
        return jsonify({"error": "Failed to fetch stats"}), 404



@app.route("/")
def health():
    """Health check."""
    try:
        return jsonify({"status": "ok"}), 200
    except Exception:
        return jsonify({"error": "Health check failed"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
