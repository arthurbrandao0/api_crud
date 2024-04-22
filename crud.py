from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn


# Criar a tabela se não existir
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Rota para criar um novo usuário
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

# Rota para obter todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    users_list = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
    return jsonify(users_list)

# Rota para obter um usuário por ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_data = {"id": user[0], "name": user[1], "email": user[2]}
        return jsonify(user_data)
    else:
        return jsonify({"message": "User not found"}), 404

# Rota para atualizar um usuário por ID
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated successfully"})

# Rota para deletar um usuário por ID
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"})


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
