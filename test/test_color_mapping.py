import unittest
import color_mapping

class TestColorMapping(unittest.TestCase):

    def test_apply_color_map(self):
        test_frame = [0, 128, 255]
        result = color_mapping.apply_color_map(test_frame)
        self.assertIsInstance(result, str)  # Check if result is a string (base64)

if __name__ == '__main__':
    unittest.main()
