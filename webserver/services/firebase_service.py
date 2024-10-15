import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firebase():
    if not firebase_admin._apps:
        firebase_creds = {
            "type": os.environ.get('firebase_type'),
            "project_id": os.environ.get('firebase_project_id'),
            "private_key_id": os.environ.get('firebase_private_key_id'),
            "private_key": os.environ.get('firebase_private_key').replace("\\n", "\n"),  
            "client_email": os.environ.get('firebase_client_email'),
            "client_id": os.environ.get('firebase_client_id'),
            "auth_uri": os.environ.get('firebase_auth_uri'),
            "token_uri": os.environ.get('firebase_token_uri'),
            "auth_provider_x509_cert_url": os.environ.get('firebase_auth_provider_x509_cert_url'),
            "client_x509_cert_url": os.environ.get('firebase_client_x509_cert_url')
        }
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)

# Call this function to initialize Firebase
init_firebase()
db = firestore.client()

def save_video_to_firebase(user_id, video_id, url, transcription, summary, video_name):
    doc_ref = db.collection('users').document(user_id).collection('videos').document(video_id)
    doc_ref.set({
        'url': url,
        'transcription': transcription,
        'summary': summary,
        'name': video_name  
    })

def check_existing_video_data(user_id, video_id):
    doc_ref = db.collection('users').document(user_id).collection('videos').document(video_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

def check_all_videos_for_user(user_id):
    collection_ref = db.collection('users').document(user_id).collection('videos')
    docs = collection_ref.stream()
    return docs
