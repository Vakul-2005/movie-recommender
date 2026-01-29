# 🎬  AI Movie Recommender
movie-recommender/
│
├─ app.py                # Main Streamlit app
├─ background.png        # Netflix-style background
├─ requirements.txt      # Dependencies
├─ .gitignore            # Files/folders to ignore in Git
└─ readme.md             # Project documentation

A modern movie recommendation web app built with **Streamlit** and **TMDB API**.  
It provides:

- ✅ Movie search (manual & autocomplete style)  
- ✅ Popular movies by genres (Action, Drama, Sci-Fi)  
- ✅ AI-based similar movie recommendations using **TF-IDF & Cosine Similarity**  
- ⭐ Ratings displayed for each movie  
- 🎨 Netflix-like UI with **cool fonts, hover animations, and dark background**

---

## 📦 Features

- **Search movies**: Type a movie name or select from a list.  
- **Genres**: View popular movies by genre in horizontal scrollable cards.  
- **AI Recommendations**: Select a movie and get 5 similar movies using AI.  
- **Animations & Fonts**:  
  - Hover effects on movie posters  
  - Red glowing fonts for AI recommendation section  
  - Smooth fade-in animations  
- **Responsive UI**: Works on wide and standard screens.

---

## 🛠️ Tech Stack

- **Python 3.10+**  
- **Streamlit** for UI  
- **TMDB API** for movie data  
- **Scikit-learn** for TF-IDF & cosine similarity  
- **Base64** for safe background image embedding  
- **CSS** for fonts, animations, and Netflix-style effects  

---

## ⚡ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/netflix-ai-recommender.git
cd netflix-ai-recommender
