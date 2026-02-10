# 🍿 Mood-Based Bollywood Movie Recommender

An intelligent, mood-aware movie recommendation web app built with **Streamlit** + **Google Gemini AI** that suggests Bollywood films based on how you're feeling right now — including support for mixed/complex emotions.

## ✨ Features

- Real-time mood detection from text or emoji input using **Google Gemini**
- Supports **single** and **multiple emotions** (e.g. "sad and romantic", "tired but hopeful")
- Dynamically suggests 1–3 categories + min rating + year range
- Warm, personalized recommendation reason shown prominently
- Sidebar filters: multi-select categories, actor/actress, year from, min rating
- "Reset to AI suggestion" button
- Clean pagination (10 movies per page)
- Beautiful UI with mood emojis, highlighted reason box, expandable movie cards

## 🚀 Demo

*(Add a live link here when deployed)*  
Live Demo: https://your-app-name.streamlit.app

## Screenshots

*(You can replace these with real screenshots later)*

| Mood Input                          | Detected Mood & Reason                             | Movie Results (paginated)                     |
|-------------------------------------|----------------------------------------------------|-----------------------------------------------|
| "I'm feeling low today 😔"          | Sad 😔 + uplifting reason                          | Drama/Comedy movies with high ratings         |
| "tired but romantic 💕😓"           | Stressed + Romantic → gentle romantic dramas       | Filtered & sorted results                     |

## Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io) 1.38+
- **AI / Mood Analysis**: [Google Gemini](https://ai.google.dev) (gemini-2.5-flash-lite)
- **Data**: Pandas
- **Environment**: python-dotenv

## Project Structure
mood-based-bollywood-recommender/
├── app.py                      # Main Streamlit application
├── bollywood_movies_merged.csv # Your movie dataset (not committed)
├── .env.example                # Template for API keys
├── requirements.txt
├── .gitignore
└── README.md
text## Installation & Setup

### 1. Clone the repository

git clone https://github.com/YOUR-USERNAME/mood-based-bollywood-recommender.git
cd mood-based-bollywood-recommender

2. Create virtual environment (recommended)
   python -m venv venv

# Windows
venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

5. Add your Gemini API key
   Create .env file in root
   envGEMINI_API_KEY=your_gemini_api_key_here
You can get a free API key from: https://aistudio.google.com/app/apikey

7. Prepare your movie dataset
Make sure bollywood_movies_merged.csv exists in the root with at least these columns:

Movie Name
Year
Rating
Category
Actor
Actress

6. Run the app
Bashstreamlit run app.py
