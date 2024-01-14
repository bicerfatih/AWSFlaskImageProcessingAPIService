# AWS EC2 Flask Image Processing API

## Project Description
This repository contains a Flask-based API designed for image processing. With the deployment on AWS EC2, the application offers functionalities like image resizing, color mapping, and data handling through a SQLite database, making it ideal for cloud-based image processing solutions.

## Features
- **Image Resizing**: Automatically adjusts image sizes while maintaining aspect ratios. (In our case adjustment is 1x150 pixels from 1x200 pixels)
- **Color Mapping**: Applies color mapping on grayscale images with based on pixel intensity.
- **Database Management**: Efficiently stores and retrieves image data using SQLite.
- **Flask API**: Provides an API for easy access to processed images.
- **AWS EC2 Deployment**: Optimized for deployment in AWS EC2 environment, ensuring scalability and performance.

## Installation

1. **Clone the Repository**:
    ```
    git clone <repository-url>
    ```

2. **Navigate to the Project Directory**:
    ```
    cd flask-image-processing-api
    ```

3. **Install Dependencies**:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask application:
    ```
    python main.py
    ```

2. Access the API endpoints, for example:
    ```
    GET /get_frames?depth_min=0.5&depth_max=2.0
    ```

## API Reference

### Get Frames

**`GET /get_frames`**

Fetches processed images based on depth range.

| Parameter   | Type    | Description                       |
|-------------|---------|-----------------------------------|
| `depth_min` | float   | Minimum depth value.              |
| `depth_max` | float   | Maximum depth value.              |

## Testing

Run the following command to execute tests:

