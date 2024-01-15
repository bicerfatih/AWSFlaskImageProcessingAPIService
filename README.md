# AWS EC2 Flask Image Processing API

## Project Description
This repository contains a Flask-based API designed for image processing. With the deployment on AWS EC2, the application offers functionalities like image resizing, color mapping, and data handling through a SQLite database, making it ideal for cloud-based image processing solutions.

Please follow the steps in Deploy_Run_FlaskAPI_AWS_EC2/Deploy_Run_FlaskAPI_AWS_EC2.md file for AWS EC2 Deployment.

## Features
- **Image Resizing**: Automatically adjusts image sizes while maintaining aspect ratios. (In our case adjustment is from 1x200 pixels to 1x150 pixels for the each frame.)
- **Color Mapping**: Applies color mapping on grayscale images with based on pixel intensity.
- **Database Management**: Efficiently stores and retrieves image data using SQLite.
- **Flask API**: Provides an API for easy access to processed images. It returns resized and color_mapped image data in base64 and also saves the retrieving processed image into 
the directory as a png image file. 
- **AWS EC2 Deployment**: Optimized for deployment in AWS EC2 environment, ensuring scalability and performance. Please follow the steps in Deploy_Run_FlaskAPI_AWS_EC2 folder Deploy_Run_FlaskAPI_AWS_EC2.md file.

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
    http://127.0.0.1:8000/get_frames?depth_min=9011.1&depth_max=9011.5)
    ```

## API Reference

### Get Frames

**`/get_frames`**

Fetches processed images based on depth range.

| Parameter   | Type    | Description                       |
|-------------|---------|-----------------------------------|
| `depth_min` | float   | Minimum depth value.              |
| `depth_max` | float   | Maximum depth value.              |

## Testing

To run the tests, navigate to the project root directory and execute the following command:

python -m unittest discover -s test

This command will automatically discover and run all tests within the test directory. Ensure that each component of the application (image resizing, database management, color mapping, and API functionality) has corresponding test cases in separate files under this directory.

## AWS EC2 Deployment 

Deployment in AWS Ubuntu EC2 environment. Ensuring scalability and performance. Please follow the steps in Deploy_Run_FlaskAPI_AWS_EC2 folder Deploy_Run_FlaskAPI_AWS_EC2.md file.


Access the API endpoints, for example:
    ```
    http://<Public IPv4 address here>:8000/get_frames?depth_min=9000.1&depth_max=9000.5)
    ```
This will retrieve the first 5 rows of processed image data. User can change the depth_min and depth_max values.

## Contributing

Contributions to this project are welcome. Please adhere to this project's code of conduct while contributing.

## License

MIT

## Contact
For support or queries, reach out to me https://www.linkedin.com/in/bicerfatih/.
