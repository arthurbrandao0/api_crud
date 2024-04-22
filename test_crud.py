import unittest
import json
import sqlite3
from crud import app, create_table


class TestAPI(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        # Criar a tabela antes de executar os testes
        create_table()

    def tearDown(self):
        # Limpar a tabela após os testes
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()

    def test_create_user(self):
        data = {'name': 'Test User', 'email': 'test@example.com'}
        response = self.app.post('/user', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_user(self):
        # Adicionar um usuário para buscar
        self.app.post('/user', json={'name': 'Test User', 'email': 'test@example.com'})
        response = self.app.get('/user/3')
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.data)
        self.assertEqual(user_data['id'], 3)

    def test_update_user(self):
        # Adicionar um usuário para atualizar
        self.app.post('/user', json={'name': 'Test User', 'email': 'test@example.com'})
        data = {'name': 'Updated User', 'email': 'updated@example.com'}
        response = self.app.put('/user/1', json=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        # Adicionar um usuário para deletar
        self.app.post('/user', json={'name': 'Test User', 'email': 'test@example.com'})
        response = self.app.delete('/user/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
