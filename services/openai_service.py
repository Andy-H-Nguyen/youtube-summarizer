from openai import OpenAI
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ['openai_api_key'])

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
