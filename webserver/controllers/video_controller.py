from services.youtube_service import download_youtube_video
from services.openai_service import summarize_video_with_memory
from utils.vision_utils import extract_text_from_video
from models.video_model import save_video_to_firebase
import whisper
from typing import Dict, List

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

def save_video_data(user_id, video_id, url, transcription, summary, video_name):
    save_video_to_firebase(user_id, video_id, url, transcription, summary, video_name)