1. 🎬 Bollywood Movie Chatbot

A Streamlit application to filter and browse Bollywood movies by category, actor, actress, year, and rating with an interactive and user-friendly UI.

2. Features

- Easy-to-use dropdown filters for movie Category, Actor, Actress, Year, and Rating.
- Structured, collapsible cards showing detailed movie information.
- Emoji-enhanced user interface for an engaging experience.
- Uses a CSV dataset with Bollywood movie data.

3. Prerequisites

- Python 3.7+
- Streamlit
- pandas

4. Installation

1. Clone the repository:
git clone https://github.com/yourusername/bollywood-movie-chatbot.git
cd bollywood-movie-chatbot

2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install required packages:
pip install streamlit pandas

4. Place your `bollywood_movies_merged.csv` dataset file in the project directory.

5. Run the App

streamlit run your_script.py

Replace `your_script.py` with the name of the main Python file.

6. Project Structure

- `your_script.py` - Main Streamlit app script.
- `bollywood_movies_merged.csv` - Movie dataset.
- `.gitignore` - Git ignore rules.