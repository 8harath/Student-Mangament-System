from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name TEXT NOT NULL,
                  last_name TEXT NOT NULL,
                  email TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (first_name, last_name, email) VALUES (?, ?, ?)",
                  (data['first_name'], data['last_name'], data['email']))
        conn.commit()
        return jsonify({"message": "Student added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()

@app.route('/update_student', methods=['PUT'])
def update_student():
    data = request.json
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE students SET first_name=?, last_name=?, email=? WHERE id=?",
                  (data['first_name'], data['last_name'], data['email'], data['id']))
        conn.commit()
        if c.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": "Student updated successfully"}), 200
    finally:
        conn.close()

@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        if c.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": "Student deleted successfully"}), 200
    finally:
        conn.close()

@app.route('/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = [{"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(students), 200

if __name__ == '__main__':
    app.run(debug=True)