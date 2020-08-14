"""Модуль юнит-теста. Проверяет код ответа фласка, проверяет тестовую страницу."""
import unittest
import os
import sys
import inspect
import web_view as tested_app

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)


class FlaskAppTests(unittest.TestCase):
    """Класс юнит-теста."""

    def setUp(self):
        """Инициализация."""
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_get_hello_endpoint(self):
        """Проверка на доступность тестовой страницы."""
        resp = self.app.get('/unit_test')
        self.assertEqual(resp.data, b'Hello World!')

    def test_post_hello_endpoint(self):
        """Проверка на отклик - должен выдать код 200 у главной страницы, при успешном запуске
         Фласка."""
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
