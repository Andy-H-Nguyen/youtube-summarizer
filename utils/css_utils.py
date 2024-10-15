import streamlit as st

def inject_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #1f1f1f 0%, #3a3a3a 100%);
        color: #ffffff;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    .main-title {
        color: #ff4757;
        text-align: center;
        font-size: 3.8em;
        font-weight: bold;
        margin-top: 30px;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
        animation: fadeIn 1.5s ease-in-out;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
    }
    .main-title img {
        height: 55px;
        width: 80px;
    }
    .input-container {
        margin-top: 40px;
        padding: 35px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        animation: fadeIn 2s ease-in-out;
    }
    .input-container:hover {
        box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.6);
        transform: scale(1.02);
    }
    input, select {
        font-size: 1.4em;
        padding: 12px;
        border: none;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        margin-bottom: 25px;
        width: 100%;
    }
    input::placeholder {
        color: #cccccc;
    }
    .button {
        background: linear-gradient(135deg, #ff6348 0%, #ff7f50 100%);
        border: none;
        color: white;
        padding: 18px 36px;
        text-align: center;
        font-size: 1.3em;
        border-radius: 15px;
        cursor: pointer;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }
    .button:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 30px rgba(255, 99, 72, 0.6);
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-size: 1.1em;
        color: #bdc3c7;
        animation: fadeIn 2s ease-in-out;
    }
    .placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 704px;
        height: 528px;
        border: 2px dashed #7f8c8d;
        border-radius: 20px;
        color: #7f8c8d;
        font-size: 1.6em;
        margin-bottom: 25px;
        animation: fadeIn 2s ease-in-out;
    }
    .transcription-box, .summary-box {
        background-color: #353535;
        padding: 25px;
        border-radius: 15px;
        color: #ecf0f1;
        font-size: 1.2em;
        line-height: 1.8;
        margin-top: 25px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
        word-wrap: break-word;
        animation: fadeIn 2s ease-in-out;
    }
    .stExpander .stTextInput .stElementContainer {
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
