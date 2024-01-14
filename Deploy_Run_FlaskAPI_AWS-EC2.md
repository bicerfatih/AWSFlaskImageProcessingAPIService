# Deploy and Run Flask App on AWS EC2 Instance

Install Python Virtualenv
```bash
sudo apt-get update
sudo apt-get install python3-venv
```
Activate the new virtual environment in a new directory

Create directory
```bash
mkdir myFlaskAPI
cd helloworld
```
Create the virtual environment
```bash
python3 -m venv venv
```
Activate the virtual environment
```bash
source venv/bin/activate
```
Install Flask
```bash
pip install Flask
```
Create a Simple Flask API
```bash
sudo nano app.py
```
```bash
// Add this to main.py
from flask import Flask, request, jsonify
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from PIL import Image

# Resize

def resize_frame_1d(frame_series, new_length):
    # Convert the series to a numpy array
    frame_array = frame_series.values

    # Resize the 1x200 frame to the new length
    resized_frame = np.array(Image.fromarray(frame_array.reshape((1, -1))).resize((new_length, 1)))

    # Flatten the resized frame back.
    return resized_frame.flatten()

def resize_frames_in_csv_1d(csv_path, new_length, output_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Resizing all frames
    resized_frames = df.apply(lambda row: resize_frame_1d(row[1:], new_length), axis=1)

    # Creating a new DataFrame for the resized frames
    resized_df = pd.DataFrame(resized_frames.tolist(), index=df.index)
    resized_df.columns = [f'col{i+1}' for i in range(new_length)]
    resized_df.insert(0, 'depth', df['depth'])

    # Saving the resized frames as a new CSV file
    resized_df.to_csv(output_path, index=False)

# Example usage
csv_path = 'img.csv'  # Replace with your CSV file path
new_length = 150
output_path = 'resized_csv9.csv'  # Replace with your desired output file path

resize_frames_in_csv_1d(csv_path, new_length, output_path)


# Database

csv_file = 'resized_csv.csv'

# Create a new SQLite database
db_connection = sqlite3.connect('images.db')

# Create a table for storing image data
# Dynamically creating column definitions for each pixel value
columns = ', '.join([f'col{i} INTEGER' for i in range(1, 151)])
create_table_query = f"""
CREATE TABLE IF NOT EXISTS image_data (
    depth REAL PRIMARY KEY,
    {columns}
);
"""
db_connection.execute(create_table_query)

# Read the resized image data from CSV
resized_data = pd.read_csv(csv_file)

# Insert data into the database
resized_data.to_sql('image_data', db_connection, if_exists='replace', index=False)

# Close the database connection
db_connection.close()

def apply_color_map(frame, colormap='jet'):
    # Convert frame to numpy array and normalize
    np_frame = np.array(frame, dtype=np.uint8)
    normalized_frame = np_frame / 255

    # Apply color map
    colored_frame = plt.get_cmap(colormap)(normalized_frame)

    # Convert to image
    plt.imshow(colored_frame, cmap=colormap)
    plt.axis('off')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return base64.b64encode(image_png).decode('utf-8')

def get_frames(depth_min, depth_max):
    # Connect to SQLite database
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    # Query to fetch frames between depth_min and depth_max
    cursor.execute("SELECT * FROM image_data WHERE depth BETWEEN ? AND ?", (depth_min, depth_max))
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert rows to a list of colorized frames
    frames = []
    for row in rows:
        frame_data = row[1:] # excluding depth value
        colorized_frame = apply_color_map(frame_data)
        frames.append({'depth': row[0], 'frame': colorized_frame})

    return frames


app = Flask(__name__)

@app.route('/get_frames', methods=['GET'])
def api_get_frames():
    depth_min = request.args.get('depth_min', type=float)
    depth_max = request.args.get('depth_max', type=float)

    # Validate inputs
    if depth_min is None or depth_max is None:
        return "Invalid request. Please specify depth_min and depth_max.", 400

    frames = get_frames(depth_min, depth_max)
    return jsonify(frames)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

```
Verify if it works by running 
```bash
python app.py
```
Run Gunicorn WSGI server to serve the Flask Application
When you “run” flask, you are actually running Werkzeug’s development WSGI server, which forward requests from a web server.
Since Werkzeug is only for development, we have to use Gunicorn, which is a production-ready WSGI server, to serve our application.

Install Gunicorn using the below command:
```bash
pip install gunicorn
```
Run Gunicorn:
```bash
gunicorn -b 0.0.0.0:8000 app:app 
```
Gunicorn is running (Ctrl + C to exit gunicorn)!

Use systemd to manage Gunicorn
Systemd is a boot manager for Linux. We are using it to restart gunicorn if the EC2 restarts or reboots for some reason.
We create a <projectname>.service file in the /etc/systemd/system folder, and specify what would happen to gunicorn when the system reboots.
We will be adding 3 parts to systemd Unit file — Unit, Service, Install

Unit — This section is for description about the project and some dependencies
Service — To specify user/group we want to run this service after. Also some information about the executables and the commands.
Install — tells systemd at which moment during boot process this service should start.
With that said, create an unit file in the /etc/systemd/system directory
	
```bash
sudo nano /etc/systemd/system/helloworld.service
```
Then add this into the file.
```bash
[Unit]
Description=Gunicorn instance for a simple hello world app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/myFlaskAPI
ExecStart=/home/ubuntu/myFlaskAPI/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target
```
Then enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start myFlaskAPI
sudo systemctl enable myFlaskAPI
```
Check if the app is running with 
```bash
curl localhost:8000
```
Run Nginx Webserver to accept and route request to Gunicorn
Finally, we set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn.

Install Nginx 
```bash
sudo apt-get nginx
```
Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the default nginx landing page
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```
Edit the default file in the sites-available folder.
```bash
sudo nano /etc/nginx/sites-available/default
```
Add the following code at the top of the file (below the default comments)
```bash
upstream myFlaskAPI {
    server 127.0.0.1:8000;
}
```
Add a proxy_pass to flaskhelloworld atlocation /
```bash
location / {
    proxy_pass http://myFlaskAPI;
}
```
Restart Nginx 
```bash
sudo systemctl restart nginx
```

