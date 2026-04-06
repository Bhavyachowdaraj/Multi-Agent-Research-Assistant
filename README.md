# Nexus AI — Multi-Agent Research Assistant

A full-featured AI research assistant web app built with Flask and Azure OpenAI. Upload PDFs, images, audio, and video files for AI-powered analysis, summarisation, and deep-dive research.

---

## Features

| Feature | Free | Pro |
|---------|------|-----|
| Unlimited text chat | ✅ | ✅ |
| PDF analysis | ✅ | ✅ |
| Image/vision analysis | ✅ | ✅ |
| Chat history (50) | ✅ | ✅ |
| Audio file analysis | ❌ | ✅ |
| Video file analysis | ❌ | ✅ |
| Unlimited history | ❌ | ✅ |

---

## Quick Start

### Prerequisites
- Python 3.9+
- An Azure OpenAI Resource (API Key, Endpoint, and Deployment Name)

### 1. Install & Run

The project includes one-click setup scripts for all platforms.

**Windows:**
Double-click `run.bat` or run in terminal:
```powershell
.\run.bat
```

**Mac / Linux:**
```bash
chmod +x run.sh
./run.sh
```

**Manual setup:**
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

### 2. Configure Environment

Edit your `.env` file to include your Azure OpenAI credentials:

```env
AZURE_OPENAI_API_KEY=your_azure_key_here
AZURE_END_POINT=https://your-resource.openai.azure.com/
AZURE_API_VERSION=2024-02-15-preview
AZURE_CHAT_DEPLOYMENT_NAME=gpt-4-turbo
SECRET_KEY=generate-a-long-random-string
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

---

## Project Structure

```
ai_research_assistant/
├── app.py                  # Flask app factory + entry point
├── requirements.txt        # Python dependencies (updated for 2026)
├── .env                    # API keys & Configuration
├── run.sh / run.bat        # One-click launch scripts
├── models/
│   └── models.py           # SQLAlchemy DB models (User, Conversation, Message)
├── routes/
│   ├── auth.py             # User authentication (Login/Register)
│   ├── chat.py             # Chat logic using Azure OpenAI (Streaming)
│   ├── upload.py           # Multi-modal file upload handler
│   └── history.py          # Session management
├── templates/              # Beautiful UI templates
└── uploads/                # Local storage for research assets
```

---

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt
- **AI Engine**: Azure OpenAI SDK (v2.x compatible)
- **Document Processing**: PyPDF2 (PDF text extraction)
- **Computer Vision**: Pillow (Image processing)
- **Frontend**: Premium Vanilla CSS + Modern Javascript

---

## Notes

- **Database**: Uses SQLite (`instance/nexus.db`) created automatically on first run.
- **Mock Mode**: If no API key is detected, Nexus will respond in demo mode to showcase the UI.
- **Production**: For live deployment, use a WSGI server like `gunicorn` and secure your `.env`.

