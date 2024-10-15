from models.video_model import check_existing_video_data, save_video_data
from controllers.transcribe_controller import transcribe_video_orchestrator

def transcribe_video(url, model, batch_size, user_id, video_id):
    existing_data = check_existing_video_data(user_id, video_id)
    if existing_data:
        return existing_data['transcription'], existing_data['summary']
    
    result = transcribe_video_orchestrator(url, model, batch_size)
    transcript = result.get('transcription')
    summary = result.get('summary')
    video_name = result.get('name')
    
    save_video_data(user_id, video_id, url, transcript, summary, video_name)
    
    return transcript, summary
