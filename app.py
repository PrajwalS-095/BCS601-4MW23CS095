from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('student.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            m1 INTEGER,
            m2 INTEGER,
            m3 INTEGER,
            m4 INTEGER,
            m5 INTEGER,
            total INTEGER,
            percentage REAL,
            grade TEXT
        )
    ''')
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        m1 = int(request.form['m1'])
        m2 = int(request.form['m2'])
        m3 = int(request.form['m3'])
        m4 = int(request.form['m4'])
        m5 = int(request.form['m5'])

        total = m1 + m2 + m3 + m4 + m5
        percentage = total / 5

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 75:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "Fail"

        conn = sqlite3.connect('student.db')
        conn.execute('''
            INSERT INTO results 
            (name, m1, m2, m3, m4, m5, total, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, m1, m2, m3, m4, m5, total, percentage, grade))
        conn.commit()
        conn.close()

        return redirect('/')

    conn = sqlite3.connect('student.db')
    data = conn.execute('SELECT * FROM results ORDER BY id DESC').fetchall()
    conn.close()

    return render_template('index.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('student.db')
    conn.execute('DELETE FROM results WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

init_db()

if __name__ == '__main__':
    app.run(debug=True)