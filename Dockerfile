# Use an official Python 3.9 slim image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies, clean up, and remove cached files
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Define the Gunicorn command to run your Flask application
CMD ["gunicorn", "--timeout", "0", "-b", "0.0.0.0:5000", "app:app"]
