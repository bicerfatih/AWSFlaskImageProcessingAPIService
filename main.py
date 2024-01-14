"""
Main Application Script
-----------------------

Image resizing, database management, color mapping, and the Flask API service.

The script performs the following tasks:
1. Resizes image frames and saves them to a new CSV file.
2. Creates SQLite database with the resized image data.
3. Starts the Flask application to serve the API endpoints.
"""

import api_service
import database_management
import image_resizing

if __name__ == "__main__":

    # Define file paths
    csv_path = '/Users/fatihbicer/PycharmProjects/pythonProject2/img.csv'
    resized_csv_path = 'resized_img.csv'
    new_length = 150

    # Resize frames and save to a new CSV
    image_resizing.resize_frames_in_csv_1d(csv_path, new_length, resized_csv_path)

    # Create database and insert resized data
    database_management.create_and_populate_db(resized_csv_path)

    # Run the Flask app
    api_service.app.run(debug=True)
