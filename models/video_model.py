import firebase_admin
from firebase_admin import credentials, firestore
from services.firebase_service import save_video_to_firebase, check_existing_video_data

if not firebase_admin._apps:
    cred = credentials.Certificate('path-to-your-firebase-serviceAccount.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_video(user_id, video_id):
    return check_existing_video_data(user_id, video_id)

def save_video_data(user_id, video_id, url, transcription, summary, video_name):
    save_video_to_firebase(user_id, video_id, url, transcription, summary, video_name)
