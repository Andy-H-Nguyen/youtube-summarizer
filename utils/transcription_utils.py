import time
from typing import List, Dict

def format_transcription(transcription: List[Dict[str, float | str]]) -> str:
    formatted_text = ""
    
    for segment in transcription:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        
        start_time_formatted = time.strftime("%H:%M:%S", time.gmtime(start_time))
        end_time_formatted = time.strftime("%H:%M:%S", time.gmtime(end_time))
        
        formatted_text += f"**{start_time_formatted} - {end_time_formatted}**: {text}\n\n"
    
    return formatted_text
