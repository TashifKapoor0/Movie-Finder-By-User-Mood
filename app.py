import streamlit as st
import pandas as pd
import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

# =========================
# Page Config (MUST BE FIRST)
# =========================
st.set_page_config(
    page_title="🎬 Mood Based Bollywood Movie Recommender",
    page_icon="🍿",
    layout="wide"
)

# =========================
# Load .env variables
# =========================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ Gemini API key not found. Please set GEMINI_API_KEY in .env file.")
    st.stop()

# =========================
# Gemini Configuration
# =========================
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# =========================
# Load Data
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("bollywood_movies_merged.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =========================
# SAFE JSON EXTRACTOR
# =========================
def extract_json(text):
    if not text:
        return None

    text = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    return None

# =========================
# Gemini → Full mood + filter suggestion (improved prompt)
# =========================
def analyze_user_mood(text):
    prompt = f"""
You are an expert Bollywood movie recommender specialized in matching moods.

User's message: "{text}"

Instructions:
- Detect the MAIN emotion(s). You can pick 1 or 2 emotions if the user clearly expresses more than one.
- Allowed emotions: sad, happy, angry, stressed, bored, romantic, nostalgic, neutral
- If user mentions two feelings (example: tired and romantic), pick the two most prominent.
- For rating and year_from → use these FIXED values (do NOT change them):

  sad       → min_rating=7.0,  year_from=null
  happy     → min_rating=6.0,  year_from=null
  angry     → min_rating=6.5,  year_from=null
  stressed  → min_rating=6.5,  year_from=null
  bored     → min_rating=6.5,  year_from=null
  romantic  → min_rating=6.5,  year_from=null
  nostalgic → min_rating=6.0,  year_from=1995
  neutral   → min_rating=6.0,  year_from=null

- If TWO emotions → use the STRICTER (higher) min_rating and the EARLIER year_from (if any)

Categories (choose 1–3 most helpful from this exact list):
Comedy, Drama, Romantic, Action, Thriller, Family, Crime, Biography, Horror, Sci-Fi, Mystery

Write a warm, short reason (1–2 sentences) explaining why these movies fit the mood(s).

Return ONLY valid JSON:

{{
  "emotions": ["sad", "romantic"],
  "categories": ["Drama", "Romantic"],
  "min_rating": 7.0,
  "year_from": null,
  "reason": "Heart-touching dramas and romantic stories can help process complex feelings of sadness mixed with longing."
}}

Few-shot examples:

User: "feeling very sad and lonely tonight 😢"
{{
  "emotions": ["sad"],
  "categories": ["Drama", "Romantic"],
  "min_rating": 7.0,
  "year_from": null,
  "reason": "Emotional dramas and touching love stories often bring comfort when you're feeling down and alone."
}}

User: "I'm tired but also in a romantic mood"
{{
  "emotions": ["stressed", "romantic"],
  "categories": ["Romantic", "Drama"],
  "min_rating": 6.5,
  "year_from": null,
  "reason": "Gentle romantic dramas are perfect for unwinding while feeding your romantic side."
}}

User: "super bored, need something exciting"
{{
  "emotions": ["bored"],
  "categories": ["Action", "Comedy"],
  "min_rating": 6.5,
  "year_from": null,
  "reason": "High-energy action and funny comedies will quickly shake off boredom."
}}
"""
    try:
        response = model.generate_content(prompt)
        parsed = extract_json(response.text)
        
        if not parsed or "emotions" not in parsed:
            raise ValueError("Invalid response")

        allowed = {"sad","happy","angry","stressed","bored","romantic","nostalgic","neutral"}
        emotions = [e for e in parsed.get("emotions", ["neutral"]) if e in allowed]
        if not emotions:
            emotions = ["neutral"]

        parsed["emotions"] = emotions
        parsed["min_rating"] = float(parsed.get("min_rating", 6.0))
        if parsed.get("year_from") is not None:
            parsed["year_from"] = int(parsed["year_from"])

        if not isinstance(parsed.get("categories"), list):
            parsed["categories"] = []

        return parsed
        
    except Exception:
        return {
            "emotions": ["neutral"],
            "categories": ["Comedy"],
            "min_rating": 6.0,
            "year_from": None,
            "reason": "Couldn't clearly understand — recommending easy-going comedies."
        }

# =========================
# Initialize Session State
# =========================
default_states = {
    "category_filter": [],
    "actor_filter": "All",
    "actress_filter": "All",
    "year_filter": 1950,
    "rating_filter": 6.0,
    "ai_filters": {},
    "page": 1,
}

for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "run_ai" not in st.session_state:
    st.session_state.run_ai = False

# =========================
# UI Header
# =========================
st.title("🍿 Mood Based Bollywood Movie Recommender")
st.markdown(
    "Write how you feel (text or emoji), click the button, and let AI understand your mood. "
    "You can always fine-tune the filters manually 🎥✨"
)

# =========================
# User Mood Input
# =========================
user_text = st.text_input(
    "🧠 How are you feeling today?",
    placeholder="Example: I am feeling low today 😔 or I'm tired but romantic",
    key="user_query",
)

if st.button("🎯 Understand my mood"):
    st.session_state.run_ai = True
    st.session_state.page = 1

# =========================
# Run AI
# =========================
if st.session_state.run_ai and st.session_state.user_query.strip():
    with st.spinner("🧠 Understanding your mood..."):
        ai_result = analyze_user_mood(st.session_state.user_query)

    st.session_state.ai_filters = ai_result
    st.session_state.category_filter = ai_result.get("categories", [])
    st.session_state.rating_filter   = ai_result.get("min_rating", 6.0)
    yf = ai_result.get("year_from")
    st.session_state.year_filter = yf if yf is not None else 1950

    st.session_state.run_ai = False
    st.rerun()

# =========================
# Sidebar Filters
# =========================
st.sidebar.header("🎛️ Filter your Movies")

all_categories = sorted(df["Category"].dropna().unique().tolist())

safe_defaults = [cat for cat in st.session_state.get("category_filter", []) if cat in all_categories]

st.sidebar.multiselect(
    "🎬 Categories",
    options=all_categories,
    default=safe_defaults,
    key="category_filter",
    placeholder="Select or let AI suggest"
)

st.sidebar.selectbox("🧑‍🎤 Actor", ["All"] + sorted(df["Actor"].dropna().unique().tolist()), key="actor_filter")
st.sidebar.selectbox("👩‍🎤 Actress", ["All"] + sorted(df["Actress"].dropna().unique().tolist()), key="actress_filter")

st.sidebar.number_input(
    "📅 From year",
    min_value=1950,
    max_value=2030,
    value=st.session_state.year_filter,
    step=1,
    key="year_filter"
)

st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=0.0,
    max_value=10.0,
    value=st.session_state.rating_filter,
    step=0.5,
    key="rating_filter"
)

if st.sidebar.button("🔄 Reset to AI suggestion"):
    ai = st.session_state.get("ai_filters", {})
    st.session_state.category_filter = ai.get("categories", [])
    st.session_state.rating_filter   = ai.get("min_rating", 6.0)
    st.session_state.year_filter     = ai.get("year_from") or 1950
    st.rerun()

# =========================
# Apply Filters
# =========================
filtered_df = df.copy()

if st.session_state.category_filter:
    filtered_df = filtered_df[filtered_df["Category"].isin(st.session_state.category_filter)]

if st.session_state.actor_filter != "All":
    filtered_df = filtered_df[filtered_df["Actor"] == st.session_state.actor_filter]

if st.session_state.actress_filter != "All":
    filtered_df = filtered_df[filtered_df["Actress"] == st.session_state.actress_filter]

if st.session_state.year_filter > 1950:
    filtered_df = filtered_df[filtered_df["Year"].astype(int) >= st.session_state.year_filter]

if st.session_state.rating_filter > 0:
    filtered_df = filtered_df[filtered_df["Rating"].astype(float) >= st.session_state.rating_filter]

filtered_df = filtered_df.sort_values(by="Rating", ascending=False)

# =========================
# Results Header
# =========================
mood_emojis = {
    "sad": "😔", "happy": "😊", "angry": "😣", "stressed": "😓",
    "bored": "🥱", "romantic": "💕", "nostalgic": "🕰️", "neutral": "😐"
}

if st.session_state.get("ai_filters", {}).get("emotions"):
    emotions = st.session_state.ai_filters["emotions"]
    emo_str = " + ".join(e.capitalize() for e in emotions)
    emo_icon = " ".join(mood_emojis.get(e, "") for e in emotions)
    st.success(f"Detected mood: **{emo_str}** {emo_icon}")

reason = st.session_state.ai_filters.get("reason", "")
if reason:
    st.markdown(
        f"""
        <div style="background-color:#f0f8ff; padding:18px; border-radius:12px; border-left:6px solid #1e90ff; margin:16px 0;">
            <strong style="font-size:1.1em;">Why these movies?</strong><br>
            {reason}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(f"### 🎬 Showing {len(filtered_df)} movie(s) total")

# =========================
# Display Movies
# =========================
PAGE_SIZE = 10
total_movies = len(filtered_df)
total_pages = max(1, (total_movies - 1) // PAGE_SIZE + 1)

st.session_state.page = max(1, min(st.session_state.page, total_pages))

start = (st.session_state.page - 1) * PAGE_SIZE
end = start + PAGE_SIZE

paginated_df = filtered_df.iloc[start:end]

if not paginated_df.empty:
    for _, row in paginated_df.iterrows():
        with st.expander(f"{row['Movie Name']} ({row['Year']}) ⭐ {row['Rating']}"):
            st.markdown(
                f"""
                <div style="padding: 10px 18px; background-color: #f8f9fa; border-radius: 12px;">
                    <p><strong>🎬 Movie:</strong> {row['Movie Name']}</p>
                    <p><strong>🎭 Category:</strong> {row['Category']}</p>
                    <p><strong>🧑‍🎤 Actor:</strong> {row['Actor']}</p>
                    <p><strong>👩‍🎤 Actress:</strong> {row['Actress']}</p>
                    <p><strong>📅 Year:</strong> {row['Year']}</p>
                    <p><strong>⭐ Rating:</strong> {row['Rating']}</p>
                    <p><strong>🧠 Why recommended?</strong> {st.session_state.ai_filters.get('reason','')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("😕 No movies found. Try adjusting filters or your mood description.")

# =========================
# Pagination (moved to bottom)
# =========================
if total_movies > 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Previous", disabled=st.session_state.page <= 1, key="prev_bottom"):
            st.session_state.page -= 1
            st.rerun()

    with col2:
        st.markdown(f"<div style='text-align:center; font-weight:bold;'>Page {st.session_state.page} of {total_pages} • {len(paginated_df)} movies this page</div>", unsafe_allow_html=True)

    with col3:
        if st.button("Next →", disabled=st.session_state.page >= total_pages, key="next_bottom"):
            st.session_state.page += 1
            st.rerun()

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit + Gemini AI")
