### Overview:
This project provides a streamlined solution to convert YouTube videos into reels, optimized for social media sharing. It trims the video while streaming, converts it to a reel size on-the-fly to reduce disk space loss, and adds hardcoded subtitles by converting audio to text.

### Process:
- **Input**: YouTube link.
- **Processing**:
  - Trims video while streaming.
  - Converts it to a reel size to minimize disk space usage.
  - Converts audio to text and overlays it as hardcoded subtitles onto the video.
- **Output**: Reel.

### Prerequisites:
Ensure Docker is installed and globally accessible.

### Usage:
1. Clone this repository.
2. Navigate to the project directory.
3. Build the Docker image using:
    ```
    docker build -t your_image_name .
    ```
4. Run the Docker container:
    ```
    docker run -p 5000:5000 your_image_name
    ```

### Instructions:
1. Input a YouTube link.
2. The system will process the video in real-time.
3. Access the resulting reel optimized for social media sharing.
