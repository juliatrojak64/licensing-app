import unittest
from app import app

class TestAPIRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_user_stages(self):
        response = self.app.get('/stages-overview/1')
        self.assertEqual(response.status_code, 200)

    def test_get_current_stage(self):
        response = self.app.get('/current-stage/1')
        self.assertEqual(response.status_code, 200)

    def test_estimate_completion_times(self):
        response = self.app.get('/time-estimation/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
