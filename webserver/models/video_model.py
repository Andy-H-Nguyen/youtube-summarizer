import firebase_admin
from firebase_admin import credentials, firestore
from services.firebase_service import save_video_to_firebase

if not firebase_admin._apps:
    cred = credentials.Certificate('path-to-your-firebase-serviceAccount.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def check_existing_video_data(user_id, video_id):
    doc_ref = db.collection('users').document(user_id).collection('videos').document(video_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def save_video_data(user_id, video_id, url, transcription, summary, video_name):
    save_video_to_firebase(user_id, video_id, url, transcription, summary, video_name)
