import unittest
import FlaskPNHIA as tested_app
import sys
sys.path.insert(1,'../../FlaskPNHIA.py')
import FlaskPNHIA


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_get_hello_endpoint(self):
        r = self.app.get('/unit_test')
        self.assertEqual(r.data, b'Hello World!')

    def test_post_hello_endpoint(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
