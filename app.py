from flask import Flask, request, render_template, redirect, flash, url_for, send_from_directory
from pytube import YouTube
import subprocess
import os
from pytube.exceptions import VideoUnavailable, RegexMatchError
from slugify import slugify
from datetime import timedelta
import whisper
import random


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure the directories exist
if not os.path.exists("static"):
    os.makedirs("static")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def transcribe_audio(audio_path, video_filename):
    model = whisper.load_model("base")  # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=audio_path)
    segments = transcribe['segments']
    srt_filename = os.path.join("static", f"{video_filename}.srt")

    with open(srt_filename, 'w', encoding='utf-8') as srt_file:
        for segment in segments:
            startTime = str(0) + str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0) + str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id'] + 1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

            srtFilename = os.path.join("static", f"{video_filename}.srt")
            with open(srtFilename, 'a', encoding='utf-8') as srtFile:
                srtFile.write(segment)

    return srt_filename

def overlay_subtitle(video_path, subtitle_path, outline_color):
    output_video_path = video_path.replace(".mp4", "subtitles.mp4")
    # Perform the ffmpeg command to overlay subtitles
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vf',
        f"subtitles={subtitle_path}:force_style='PrimaryColour=&H000000,SecondaryColour=&H000000,OutlineColour={outline_color},BackColour=&H000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=25,Fontname=Arial,Fontsize=16,Alignment=2'",
        output_video_path
    ]
    subprocess.run(ffmpeg_cmd)

    return output_video_path
def reverse_hex_color_with_prefix(color):
    # Check if the color starts with '#'
    if color.startswith('#'):
        color = color[1:]  # Remove the '#' character

    # Reverse the color by swapping the order of RGB components
    reversed_color = color[4:] + color[2:4] + color[:2]

    # Add the '&H' prefix
    reversed_color = '&H' + reversed_color

    return reversed_color


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        outline_color = request.form['color']
        outline_color = reverse_hex_color_with_prefix(outline_color)
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            if not stream:
                flash("No suitable streams found.")
                return redirect(request.url)

            video_title = slugify(yt.title)
            video_filename = f"{video_title}.mp4"
            video_output_path = os.path.join("static", video_filename)
            video_duration = yt.length  # Duration in seconds

            # Generate a random start time within the video duration
            start_time = random.randint(0, video_duration - 15)

            # Define the end time as 15 seconds after the start time
            end_time = min(start_time + 15, video_duration)

            cmd = [
                'ffmpeg',
                '-i', stream.url,
                '-ss', str(start_time),
                '-t', str(end_time - start_time),  
                '-vf', 'crop=ih*(9/16):ih',
                '-vcodec', 'libx264',
                video_output_path
            ]
            subprocess.run(cmd)

            subtitle_path = transcribe_audio(video_output_path, video_title)

            output_video_path = overlay_subtitle(video_output_path, subtitle_path, outline_color)
 
            return redirect(url_for('video_page', video_path=output_video_path, subtitle_path=subtitle_path))

        except (VideoUnavailable, RegexMatchError) as e:
            flash("Video is unavailable or not found.")
        except Exception as e:
            flash(f"Error: {str(e)}")

    return render_template('index.html', video_path=None, subtitle_path=None)

@app.route('/video_page', methods=['GET'])
def video_page():
    video_path = request.args.get('video_path', None)
    subtitle_path = request.args.get('subtitle_path', None)

    return render_template('video_page.html', video_path=video_path, subtitle_path=subtitle_path)

@app.route('/edit_subtitle', methods=['GET', 'POST'])
def edit_subtitle():
    if request.method == 'POST':
        edited_subtitle_content = request.form['edited_subtitle']
        subtitle_path = request.form['subtitle_path']
        outline_color = request.form['color']

        with open(subtitle_path, 'w', encoding='utf-8') as subtitle_file:
            subtitle_file.write(edited_subtitle_content)

        return redirect(url_for('re_run_overlay', subtitle_path=subtitle_path,color=outline_color))

    else:
        subtitle_path = request.args.get('subtitle_path')
        subtitle_content = None
        with open(subtitle_path, 'r') as subtitle_file:
            subtitle_content = subtitle_file.read()

        return render_template('edit_subtitle.html', subtitle_path=subtitle_path, subtitle_content=subtitle_content)

@app.route('/re_run_overlay', methods=['GET'])
def re_run_overlay():
    subtitle_path = request.args.get('subtitle_path')
    video_path = subtitle_path.replace(".srt", ".mp4")
    outline_color = request.args.get('color')
    reverse_outline_color = reverse_hex_color_with_prefix(outline_color)    
    video_path = overlay_subtitle(video_path, subtitle_path, reverse_outline_color )
    video_path += f"?v={random.randint(1, 1000000)}"


    return redirect(url_for('video_page', video_path=video_path, subtitle_path=subtitle_path))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
