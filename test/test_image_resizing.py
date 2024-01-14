import unittest
import image_resizing
import numpy as np

class TestImageResizing(unittest.TestCase):

    def test_resize_frame_1d(self):
        original_frame = np.arange(200)  # Example original frame
        new_length = 150
        resized_frame = image_resizing.resize_frame_1d(original_frame, new_length)
        self.assertEqual(len(resized_frame), new_length)

if __name__ == '__main__':
    unittest.main()
