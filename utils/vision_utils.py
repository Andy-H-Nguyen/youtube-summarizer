import pytesseract
import cv2
from typing import List, Dict

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
