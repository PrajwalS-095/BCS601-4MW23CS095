from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('notes.db')
    conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    conn = sqlite3.connect('notes.db')
    conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('notes.db')
    conn.execute('DELETE FROM notes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)