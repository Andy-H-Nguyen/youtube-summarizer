import tempfile
import ssl
import yt_dlp
from pprint import pprint
from typing import Dict, List
import os
import whisper
import cv2
import pytesseract
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ['openai_api_key'])

def summarize_video_with_memory(transcription_with_timestamps: List[Dict[str, float | str]], model_name: str = "gpt-3.5-turbo", batch_size: int = 5) -> str:
    messages = [{"role": "system", "content": "You are a helpful assistant that summarizes video transcripts."}]
    partial_summaries = []
    
    for i in range(0, len(transcription_with_timestamps), batch_size):
        batch = transcription_with_timestamps[i:i + batch_size]
        batch_text = "\n\n".join(
            f"From {segment['start']}s to {segment['end']}s: {segment['text']}"
            for segment in batch
        )
        messages.append({"role": "user", "content": batch_text})
        messages.append({"role": "user", "content": "Please summarize this part."})

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7
        )
        
        print(response)

        batch_summary = response.choices[0].message.content
        partial_summaries.append(batch_summary)

        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes video transcripts."},
            {"role": "assistant", "content": batch_summary}
        ]

    combined_summaries = "\n\n".join(partial_summaries)
    return combined_summaries

ssl._create_default_https_context = ssl._create_stdlib_context

def transcribe_video_orchestrator(youtube_url: str, model_name: str) -> List[Dict[str, float | str]]:
    video = download_youtube_video(youtube_url)
    transcription = transcribe(video, model_name)
    extracted_text = extract_text_from_video(video['path'], interval=5)

    for timestamp, text in extracted_text.items():
        print(f"Timestamp {timestamp:.2f}s: {text}")

    return summarize_video_with_memory(transcription)

def transcribe(video: Dict[str, str], model_name: str = "medium", hasTimestamps: bool = True) -> List[Dict[str, float | str]]:
    print(f"Transcribing '{video['name']}' using model: {model_name}")

    model = whisper.load_model(model_name)

    if hasTimestamps:
        result = model.transcribe(video['path'], verbose=True)
        transcription_with_timestamps = [
            {
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            }
            for segment in result["segments"]
        ]
        pprint(transcription_with_timestamps)
        return transcription_with_timestamps
    else:
        result = model.transcribe(video['path'])
        pprint(result)
        return result["text"]

def download_youtube_video(youtube_url: str) -> dict:
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': tempfile.gettempdir() + '/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        file_path = ydl.prepare_filename(info)
        print(f"Download complete: {file_path}")
        return {
            "name": info.get('title', 'Unknown Title'),
            "thumbnail": info.get('thumbnail'),
            "path": file_path
        }

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Download progress: {round(pct_completed, 2)}%")

def extract_text_from_video(video_path: str, interval: int = 5):
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    frame_interval = int(frame_rate * interval)
    current_frame = 0

    text_data = {}

    while True:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        success, frame = video_capture.read()
        if not success:
            break

        timestamp = current_frame / frame_rate
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_frame)
        print(f"Timestamp {timestamp:.2f}s: {text}")
        text_data[timestamp] = text.strip()
        current_frame += frame_interval

    video_capture.release()
    print(f"Frame Transcription With Interval={interval}")
    pprint(text_data)

    return text_data
