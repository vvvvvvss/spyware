import time
import os
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set the server URL to the local machine running the Flask server
SERVER_URL = "http://host.docker.internal:5000/upload"  # Points to the host machine from inside Docker
WATCHED_FOLDER = "/app/images"  # Folder to monitor inside the container

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the new file is an image (jpg, png, etc.)
        if event.src_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"New image detected: {event.src_path}")
            # Send the image to the server
            self.send_image(event.src_path)

    def send_image(self, image_path):
        # Open the image file and send it via POST request
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            try:
                response = requests.post(SERVER_URL, files=files)
                if response.status_code == 200:
                    print(f"Successfully sent {image_path}")
                else:
                    print(f"Failed to send {image_path}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error sending image: {e}")

if __name__ == "__main__":
    # Create the directory if it doesn't exist
    if not os.path.exists(WATCHED_FOLDER):
        os.makedirs(WATCHED_FOLDER)

    # Initialize the event handler and observer
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCHED_FOLDER, recursive=False)

    # Start the observer
    observer.start()
    print(f"Monitoring folder: {WATCHED_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
