import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # For dict-like results
    return conn

def create_table():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                amount_due REAL NOT NULL
            )
        ''')
        conn.commit()


# Create
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    with get_db() as conn:
        conn.execute('''
            INSERT INTO students (first_name, last_name, dob, amount_due)
            VALUES (?, ?, ?, ?)
        ''', (data['first_name'], data['last_name'], data['dob'], data['amount_due']))
        conn.commit()
    return jsonify({'message': 'Student added'})

# Read one
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (id,)).fetchone()
    if student is None:
        return jsonify({'message': 'Not found'}), 404
    return jsonify(dict(student))

# Read all
@app.route('/students', methods=['GET'])
def get_all_students():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    return jsonify([dict(row) for row in students])

# Update
@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    with get_db() as conn:
        conn.execute('''
            UPDATE students SET first_name = ?, last_name = ?, dob = ?, amount_due = ?
            WHERE student_id = ?
        ''', (data['first_name'], data['last_name'], data['dob'], data['amount_due'], id))
        conn.commit()
    return jsonify({'message': 'Student updated'})

# Delete
@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    with get_db() as conn:
        conn.execute('DELETE FROM students WHERE student_id = ?', (id,))
        conn.commit()
    return jsonify({'message': 'Student deleted'})

if __name__ == '__main__':
    create_table()  # Call this before running the app
    app.run(debug=True)
