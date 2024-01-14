import unittest
import api_service

class TestAPIService(unittest.TestCase):

    def setUp(self):
        api_service.app.testing = True
        self.app = api_service.app.test_client()

    def test_get_frames(self):
        response = self.app.get('/get_frames?depth_min=1.0&depth_max=5.0')
        self.assertEqual(response.status_code, 200)
        # Additional checks can be added based on the expected response format

if __name__ == '__main__':
    unittest.main()