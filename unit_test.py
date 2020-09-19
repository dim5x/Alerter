"""Модуль юнит-теста. Проверяет код ответа фласка, проверяет тестовую страницу."""
import unittest
import web_view as tested_app


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

        """Проверка на отклик.

         Должен выдать код 200 у главной страницы, при успешном запуске Фласка.
         """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
