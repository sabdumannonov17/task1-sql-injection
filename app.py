#!/usr/bin/env python3
"""
SQL Injection Challenge - Backend Server (Port 5001)
"""

from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body { font-family: Arial; max-width: 400px; margin: 50px auto; padding: 20px; }
        .container { background: #f9f9f9; padding: 20px; border-radius: 10px; }
        input, button { width: 100%; padding: 10px; margin: 5px 0; }
        .error { color: red; }
        .success { color: green; }
        .flag { background: yellow; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 Admin Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        
        {% if message %}
            <div class="{{ message_type }}">{{ message }}</div>
        {% endif %}
        
        {% if flag %}
            <div class="flag">
                <strong>🏴 Flag: {{ flag }}</strong>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    
    users = [
        (1, 'admin', 'admin123', 'admin'),
        (2, 'user1', 'password1', 'user'),
        (3, 'john', 'doe123', 'user')
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
    conn.commit()
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    conn = init_db()
    cursor = conn.cursor()
    
    message = ""
    message_type = "error"
    flag = ""
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            # VULNERABLE SQL QUERY - SQL Injection possible
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                message = f"Welcome {user[1]}!"
                message_type = "success"
                
                if user[3] == 'admin':
                    flag = "WRCTF{sq1_inj3cti0n_5ucc3ss}"
                else:
                    message += " But you are not admin. No flag for you!"
            else:
                message = "Invalid username or password!"
                
        except Exception as e:
            message = f"Database error: {str(e)}"
        
        finally:
            conn.close()
    
    return render_template_string(HTML_TEMPLATE, 
                                message=message, 
                                message_type=message_type, 
                                flag=flag)


