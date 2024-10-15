
# YouTube Summarizer

YouTubeSummarizer allows you to easily convert a YouTube video into text and generate a summarized version of its content.

## Features
- Extract and transcribe YouTube videos to text.
- Generate concise summaries based on transcriptions.
- Store and retrieve previously processed videos using Firebase.

## Prerequisites
Ensure you have the following installed on your machine:
- **Python 3.8+**
- **Streamlit**
- **FFmpeg** (required for video processing)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/YouTubeSummarizer.git
cd YouTubeSummarizer
```

### 2. Set up the virtual environment and install dependencies
```bash
# Create and activate virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install FFmpeg
FFmpeg is required for video processing. Install it using the following commands based on your platform:

#### Ubuntu / Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS (using Homebrew)
```bash
brew install ffmpeg
```

#### Windows
Download and install FFmpeg from the official website: https://ffmpeg.org/download.html

### 4. Set up OpenAI API key

This project uses OpenAI's Whisper model for transcriptions and GPT-3.5 for summarization. You need an OpenAI API key to use these features.

1. Go to [OpenAI's API Keys](https://beta.openai.com/account/api-keys).
2. Create a new API key.
3. Create a `.env` file in the root directory and add the following:

```bash
OPENAI_API_KEY=your-openai-api-key
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_PRIVATE_KEY_ID=your-firebase-private-key-id
FIREBASE_PRIVATE_KEY=your-firebase-private-key
FIREBASE_CLIENT_EMAIL=your-firebase-client-email
FIREBASE_CLIENT_ID=your-firebase-client-id
FIREBASE_AUTH_URI=your-firebase-auth-uri
FIREBASE_TOKEN_URI=your-firebase-token-uri
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=your-firebase-auth-provider-x509-cert-url
FIREBASE_CLIENT_X509_CERT_URL=your-firebase-client-x509-cert-url
```

### 5. Set up Firebase

This project uses Firebase Firestore for storing and retrieving video processing data.

1. Set up a Firebase project in the [Firebase Console](https://console.firebase.google.com/).
2. Download your Firebase service account key in JSON format.
3. Save the JSON file in the `secrets` folder, and name it `serviceAccountKey.json`.

### 6. Run the application
Once all the setup is complete, you can run the application:
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser to access the app.

## License

This project is licensed under the MIT license.

## Acknowledgments

OpenAI Whisper - [OpenAI Whisper GitHub](https://github.com/openai/whisper)
