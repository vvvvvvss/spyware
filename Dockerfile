# Step 1: Use the official Python base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install necessary Python packages
RUN pip install --no-cache-dir watchdog requests

# Step 5: Define the entrypoint command to run your Python script
ENTRYPOINT ["python", "monitor_folder.py"]
