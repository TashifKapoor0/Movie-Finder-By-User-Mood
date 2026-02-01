import streamlit as st
import pandas as pd
import datetime

@st.cache_data
def load_data():
    df = pd.read_csv('bollywood_movies_merged.csv')
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.set_page_config(page_title="🎬 Bollywood Movie Chatbot", page_icon="🍿")

st.title("🍿 Bollywood Movie Chatbot")
st.markdown("Welcome! Use the filters below to find your favorite movies. Select any combination of filters as per your taste! 🎥✨")

# Sidebar Filters
st.sidebar.header("🎛️ Filter your Movies!")

categories = ['All'] + sorted(df['Category'].dropna().unique())
actors = ['All'] + sorted(df['Actor'].dropna().unique())
actresses = ['All'] + sorted(df['Actress'].dropna().unique())
years = ['All'] + sorted(df['Year'].dropna().astype(str).unique())
ratings = ['All'] + sorted(df['Rating'].dropna().astype(str).unique())

category = st.sidebar.selectbox("🎬 Category", categories)
actor = st.sidebar.selectbox("🧑‍🎤 Actor", actors)
actress = st.sidebar.selectbox("👩‍🎤 Actress", actresses)
year = st.sidebar.selectbox("📅 Year From", years)
rating = st.sidebar.selectbox("⭐ Minimum Rating", ratings)

filtered_df = df.copy()
if category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == category]
if actor != 'All':
    filtered_df = filtered_df[filtered_df['Actor'] == actor]
if actress != 'All':
    filtered_df = filtered_df[filtered_df['Actress'] == actress]

current_year = datetime.datetime.now().year
if year != 'All':
    selected_year = int(year)
    filtered_df = filtered_df[filtered_df['Year'].astype(int) >= selected_year]

if rating != 'All':
    selected_rating = float(rating)
    filtered_df = filtered_df[filtered_df['Rating'].astype(float) >= selected_rating]

st.markdown(f"### 🎬 Showing {len(filtered_df)} movie(s)")

if len(filtered_df) > 0:
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['Movie Name']} ({row['Year']}) ⭐ {row['Rating']}"):
            st.markdown(
                f"""
                <div style="padding: 10px 18px; background-color: #f8f9fa; border-radius: 12px; margin-bottom: 10px;">
                    <p><strong>🎬 Movie Name:</strong> {row['Movie Name']}</p>
                    <p><strong>🎭 Category:</strong> {row['Category']}</p>
                    <p><strong>🧑‍🎤 Actor:</strong> {row['Actor']}</p>
                    <p><strong>👩‍🎤 Actress:</strong> {row['Actress']}</p>
                    <p><strong>📅 Year:</strong> {row['Year']}</p>
                    <p><strong>⭐ Rating:</strong> {row['Rating']}</p>
                </div>
                """, unsafe_allow_html=True
            )
else:
    st.info("😕 No movies found with the selected filters. Please try a different search.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
