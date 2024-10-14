import tempfile
import ssl
import time
import yt_dlp
from pprint import pprint
from typing import Dict, List
import os
import whisper
import pytesseract
from openai import OpenAI
from dotenv import load_dotenv
try:
    import cv2
except ImportError:
    cv2 = None  # Handle the absence of OpenCV gracefully

load_dotenv()
client = OpenAI(api_key=os.environ['openai_api_key'])

import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key file
service_account_key_path = 'secrets/serviceAccountKey.json'

# Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

def save_video_data(user_id, video_id, url, transcription, summary, video_name):
    doc_ref = db.collection('users').document(user_id).collection('videos').document(video_id)
    doc_ref.set({
        'url': url,
        'transcription': transcription,
        'summary': summary,
        'name': video_name  # Store the video name in the database
    })

def check_existing_video_data(user_id, video_id):
    doc_ref = db.collection('users').document(user_id).collection('videos').document(video_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()  # Returns a dictionary with 'transcription' and 'summary'
    else:
        return None

# Retrieve all videos processed by a specific user
def check_all_videos_for_user(user_id):
    collection_ref = db.collection('users').document(user_id).collection('videos')
    docs = collection_ref.stream()  # This will return all video documents for the user
    return docs

def format_transcription(transcription):
    formatted_text = ""
    
    for segment in transcription:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        
        # Format the time to a more readable format (hh:mm:ss)
        start_time_formatted = time.strftime("%H:%M:%S", time.gmtime(start_time))
        end_time_formatted = time.strftime("%H:%M:%S", time.gmtime(end_time))
        
        # Add formatted segment to the result string
        formatted_text += f"**{start_time_formatted} - {end_time_formatted}**: {text}\n\n"
    
    return formatted_text

def summarize_video_with_memory(transcription_with_timestamps: List[Dict[str, float | str]], model_name: str = "gpt-3.5-turbo", batch_size: int = 10) -> str:
    messages = [{"role": "system", "content": "You are a helpful assistant that summarizes big tech videos. You have a transcript. Keep it concise and comprehensive."}]
    partial_summaries = []
    
    try:
        for i in range(0, len(transcription_with_timestamps), batch_size):
            batch = transcription_with_timestamps[i:i + batch_size]
            batch_text = "\n\n".join(
                f"From {segment['start']}s to {segment['end']}s: Transcription: {segment['text']}"
                for segment in batch
            )
            messages.append({"role": "user", "content": batch_text})
            messages.append({"role": "user", "content": "Please summarize this."})

            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7
            )
            
            batch_summary = response.choices[0].message.content
            partial_summaries.append(batch_summary)
        
        combined_summaries = "\n\n".join(partial_summaries)
    except Exception as e:
        print(f"An exception has occurred: {e}")
        return combined_summaries

    return combined_summaries

ssl._create_default_https_context = ssl._create_stdlib_context

def transcribe_video_orchestrator(youtube_url: str, model_name: str, batch_size: int, extract_text: bool = False) -> Dict[str, List[Dict[str, float | str]]]:
    video = download_youtube_video(youtube_url)
    transcription = transcribe(video, model_name)

    if extract_text:
        screen_text = extract_text_from_video(video['path'], transcription)
        for segment in transcription:
            end_time = segment["end"]
            segment["screen_text"] = screen_text.get(end_time, "")

    summary = summarize_video_with_memory(transcription, batch_size=batch_size)

    return {
        'summary': summary,
        'transcription': transcription,
        'name': video['name'],  # Pass the video name along with transcription and summary
    }

def transcribe(video: Dict[str, str], model_name: str = "medium", hasTimestamps: bool = True) -> List[Dict[str, float | str]]:
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
        return transcription_with_timestamps
    else:
        result = model.transcribe(video['path'])
        return result["text"]

def download_youtube_video(youtube_url: str) -> dict:
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': tempfile.gettempdir() + '/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        file_path = ydl.prepare_filename(info)
        return {
            "name": info.get('title', 'Unknown Title'),  # Extract the video name (title)
            "thumbnail": info.get('thumbnail'),
            "path": file_path
        }

def extract_text_from_video(video_path: str, transcription_with_timestamps: List[Dict[str, float | str]]) -> Dict[float, str]:
    if cv2 is None:
        print("OpenCV not available. Skipping text extraction.")
        return {}

    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video {video_path}")
        return {}

    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    text_data = {}

    for segment in transcription_with_timestamps:
        end_time = segment["end"]
        frame_number = int(end_time * frame_rate)

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = video_capture.read()
        if not success:
            continue

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_frame)
        text_data[end_time] = text.strip()

    video_capture.release()
    return text_data

