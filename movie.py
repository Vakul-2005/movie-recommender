import streamlit as st
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64

# ================= CONFIG =================
TMDB_API_KEY = "4f5e54fa74f3b3e8f0785f6499491dfc"   # <-- put your TMDB key
IMG_BASE = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="AI Movies", layout="wide")

# ================= BACKGROUND =================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
            linear-gradient(rgba(0,0,0,.88), rgba(0,0,0,.95)),
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("background.png")

# ================= STYLES =================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* TITLE */
.netflix-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4rem;
    letter-spacing: 3px;
    color: #e50914;
    text-shadow: 0 0 40px rgba(229,9,20,.8);
}

/* SECTION TITLES */
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 2px;
    margin: 30px 0 15px;
    color: white;
}

/* MOVIE CARD */
.movie-card img {
    border-radius: 14px;
    transition: all .35s ease;
}
.movie-card img:hover {
    transform: scale(1.12);
    box-shadow: 0 25px 45px rgba(229,9,20,.7);
}

/* AI CARD (STRONGER) */
.ai-card img {
    border-radius: 16px;
    transition: all .4s ease;
}
.ai-card img:hover {
    transform: scale(1.18);
    box-shadow: 0 35px 60px rgba(229,9,20,.9);
}

/* RATING */
.rating {
    color: gold;
    font-weight: 600;
}

/* CLEAN UI */
footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ================= SAFE FETCH =================
@st.cache_data(ttl=3600)
def fetch_movies(url, params):
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("results", [])
    except:
        return []

# ================= TITLE =================
st.markdown('<div class="netflix-title">🎬  AI Movie Recommender</div>', unsafe_allow_html=True)

# ================= SEARCH =================
# ================= SEARCH & SELECT =================
st.markdown('<div class="section-title">🔍 Search & Select Movie</div>', unsafe_allow_html=True)

# 1️⃣ Type to filter manually
search_term = st.text_input("Type movie name ")

# 2️⃣ Fetch movies based on search
all_movies = []
if search_term:
    results = fetch_movies(
        "https://api.themoviedb.org/3/search/movie",
        {"api_key": TMDB_API_KEY, "query": search_term, "language": "en-US", "page": 1}
    )
    all_movies.extend(results)

# 3️⃣ Multi-select list of all movie titles
if all_movies:
    movie_titles = [m.get("title") for m in all_movies if m.get("title")]
    selected_title = st.selectbox("Select a movie from the list:", movie_titles)

    # Display poster for the selected movie
    if selected_title:
        selected_movie = next(m for m in all_movies if m.get("title") == selected_title)
        st.image(IMG_BASE + selected_movie["poster_path"])
        st.caption(selected_movie.get("title"))
        st.markdown(f"<div class='rating'>⭐ {selected_movie.get('vote_average','N/A')}</div>", unsafe_allow_html=True)

# ================= GENRES (FIXED) =================
genres = {
    "Action": 28,
    "Drama": 18,
    "Sci-Fi": 878
}

for genre, gid in genres.items():
    st.markdown(f'<div class="section-title">🎞 {genre}</div>', unsafe_allow_html=True)

    movies = fetch_movies(
        "https://api.themoviedb.org/3/discover/movie",
        {
            "api_key": TMDB_API_KEY,
            "with_genres": gid,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": 1
        }
    )

    all_movies.extend(movies)

    cols = st.columns(6)
    for i, m in enumerate(movies[:12]):
        with cols[i % 6]:
            if m.get("poster_path"):
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.image(IMG_BASE + m["poster_path"])
                st.markdown('</div>', unsafe_allow_html=True)
            st.caption(m["title"])
            st.markdown(f"<div class='rating'>⭐ {m.get('vote_average','N/A')}</div>", unsafe_allow_html=True)

# ================= AI SIMILAR RECOMMENDER (NETFLIX STYLE) =================
st.divider()
st.markdown(
    """
    <style>
    .section-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.2rem;
        color: #e50914;
        text-shadow: 0 0 20px #e50914;
        animation: glow 2s infinite alternate;
        margin-top: 40px;
    }

    @keyframes glow {
        0% { text-shadow: 0 0 10px #e50914; }
        50% { text-shadow: 0 0 35px #e50914; }
        100% { text-shadow: 0 0 10px #e50914; }
    }

    .ai-card img {
        border-radius: 14px;
        transition: transform .3s ease, box-shadow .3s ease;
    }
    .ai-card img:hover {
        transform: scale(1.08) translateY(-5px);
        box-shadow: 0px 20px 40px rgba(229,9,20,.7);
    }

    .ai-rating {
        color: gold;
        font-weight: 600;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="section-title">🤖 AI Similar Movies </div>', unsafe_allow_html=True)

valid_movies = [
    m for m in all_movies
    if m.get("overview") and m.get("title")
]

if len(valid_movies) < 11:
    st.info("Search or browse more movies to activate AI recommendations.")
else:
    titles = [m["title"] for m in valid_movies]
    overviews = [m["overview"] for m in valid_movies]

    selected_movie = st.selectbox("🎬 Choose a movie", titles)

    if st.button("🎯 Recommend"):
        tfidf = TfidfVectorizer(stop_words="english", max_features=6000)
        vectors = tfidf.fit_transform(overviews)
        similarity = cosine_similarity(vectors)

        idx = titles.index(selected_movie)
        scores = sorted(
            list(enumerate(similarity[idx])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        cols = st.columns(5)
        for col, (i, _) in zip(cols, scores):
            movie = valid_movies[i]
            with col:
                if movie.get("poster_path"):
                    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
                    st.image(IMG_BASE + movie["poster_path"])
                    st.markdown('</div>', unsafe_allow_html=True)
                st.caption(movie["title"])
                st.markdown(f"<div class='rating'>⭐ {movie.get('vote_average','N/A')}</div>", unsafe_allow_html=True)
