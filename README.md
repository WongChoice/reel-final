<body>
    <h1>YouTube Reel Creator</h1>

    <h3>Overview:</h3>
    <p>This project provides a streamlined solution to convert YouTube videos into reels, optimized for social media sharing. It trims the video while streaming, converts it to a reel size on-the-fly to reduce disk space loss, and adds hardcoded subtitles by converting audio to text.</p>

    <h3>Process:</h3>
    <ul>
        <li><strong>Input</strong>: YouTube link.</li>
        <li><strong>Processing</strong>:
            <ul>
                <li>Trims video while streaming.</li>
                <li>Converts it to a reel size to minimize disk space usage.</li>
                <li>Converts audio to text and overlays it as hardcoded subtitles onto the video.</li>
            </ul>
        </li>
        <li><strong>Output</strong>: Reel.</li>
    </ul>

    <h3>Prerequisites:</h3>
    <p>Ensure Docker is installed and globally accessible.</p>

    <h3>Usage:</h3>
    <ol>
        <li>Clone this repository.</li>
        <li>Navigate to the project directory.</li>
        <li>Build the Docker image using:
            <pre><code>docker build -t your_image_name .</code></pre>
        </li>
        <li>Run the Docker container:
            <pre><code>docker run -p 5000:5000 your_image_name</code></pre>
        </li>
    </ol>

    <h3>Instructions:</h3>
    <ol>
        <li>Input a YouTube link.</li>
        <li>The system will process the video in real-time.</li>
        <li>Access the resulting reel optimized for social media sharing.</li>
    </ol>
</body>
