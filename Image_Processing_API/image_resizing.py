"""
Image Resizing Module
---------------------

This module provides functions for resizing image data. It is designed to adjust the dimensions of input images
to a specific width while maintaining their aspect ratio. This standardization is crucial for ensuring consistency
in image processing and storage.

Functions:
- resize_frame_1d(frame_series, new_length): Resizes a single frame represented as a 1D array.
- resize_frames_in_csv_1d(csv_path, new_length, output_path): Processes a CSV file containing multiple frames,
  resizing each frame.

"""

import numpy as np
import pandas as pd
from PIL import Image

def resize_frame_1d(frame_series, new_length):
    """
       Resizes a single frame represented as a 1D array.

       Parameters:
           frame_series (array-like): A 1D array or series containing pixel data of the frame.
           new_length (int): The desired new length (width) of the image after resizing.

       Returns:
           array: A flattened 1D array representing the resized frame.
       """
    frame_array = frame_series.values
    resized_frame = np.array(Image.fromarray(frame_array.reshape((1, -1))).resize((new_length, 1)))
    return resized_frame.flatten()

def resize_frames_in_csv_1d(csv_path, new_length, output_path):
    """
       Processes an entire CSV file containing multiple frames, resizing each frame.

       Usage:
           This function is typically called once to preprocess all images before they are inserted into the database.
       """
    df = pd.read_csv(csv_path)
    resized_frames = df.apply(lambda row: resize_frame_1d(row[1:], new_length), axis=1)
    resized_df = pd.DataFrame(resized_frames.tolist(), index=df.index)
    resized_df.columns = [f'col{i+1}' for i in range(new_length)]
    resized_df.insert(0, 'depth', df['depth'])
    resized_df.to_csv(output_path, index=False)