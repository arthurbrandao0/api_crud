from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Função para criar a tabela de usuários
def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Rota para criar um usuário
@app.route('/user', methods=['POST'])
def create_user():
    create_table()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    name = request.json.get('name')
    email = request.json.get('email')
    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User created successfully'}), 201

# Rota para obter todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    create_table()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return jsonify({'users': users})

# Rota para atualizar um usuário pelo ID
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    name = request.json.get('name')
    email = request.json.get('email')
    c.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, user_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated successfully'})

# Rota para excluir um usuário pelo ID
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
