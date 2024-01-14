"""
API Service Module
------------------

This module sets up and defines the Flask API for the image processing application. It provides
endpoints for clients, such as retrieving processed image data.

Functions:
- get_frames(depth_min, depth_max): Retrieves and returns color-mapped frames within a specified depth range.
"""

import sqlite3
from flask import Flask, request, jsonify
from color_mapping import apply_color_map

app = Flask(__name__)

def get_frames(depth_min, depth_max):
    """
        Retrieves and returns color-mapped frames within a specified depth range from the database.

        This endpoint processes GET requests and expects 'depth_min' and 'depth_max' parameters.

        It fetches frames from the database within the specified depth range, applies color map to each frame,
        and returns the color-mapped frames in a JSON format.

        Parameters:
            depth_min (float): Minimum depth value for the frames to retrieve.
            depth_max (float): Maximum depth value for the frames to retrieve.

        Returns:
            JSON: A list of objects with 'depth' and 'frame' (base64 encoded image data).
        """


    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM image_data WHERE depth BETWEEN ? AND ?", (depth_min, depth_max))
    rows = cursor.fetchall()
    conn.close()
    frames = []
    for row in rows:
        frame_data = row[1:]  # excluding depth value
        colorized_frame = apply_color_map(frame_data)
        frames.append({'depth': row[0], 'frame': colorized_frame})
    return frames

@app.route('/get_frames', methods=['GET'])
def api_get_frames():
    depth_min = request.args.get('depth_min', type=float)
    depth_max = request.args.get('depth_max', type=float)
    if depth_min is None or depth_max is None:
        return "Invalid request. Please specify depth_min and depth_max.", 400
    frames = get_frames(depth_min, depth_max)
    return jsonify(frames)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
