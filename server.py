from flask import Flask, request
import os

app = Flask(__name__)

# Folder to save received images
SAVE_FOLDER = "./received_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    # Get the image file from the POST request
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # Save the image to the designated folder
    file_path = os.path.join(SAVE_FOLDER, file.filename)
    file.save(file_path)
    return f"Image {file.filename} received successfully!", 200

if __name__ == "__main__":
    # Run the server on port 5000
    app.run(host='0.0.0.0', port=5000)
