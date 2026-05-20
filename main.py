from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import requests  # TMDB API se data mangwane ke liye

app = FastAPI(title="Movie Recommender API")

# CORS zaruri hai taaki frontend (HTML website) is backend se baat kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pickle files ko load karna
try:
    new_df = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    print("✅ Models loaded successfully!")
except Exception as e:
    print("⚠️ Error: Check if movies.pkl and similarity.pkl are in the same folder.")

# TMDB API Key jo tumne nikaali hai
TMDB_API_KEY = "88ce67a5b71f14307410e80933b2ce81"

def fetch_poster_and_details(movie_name):
    """Ye function TMDB ke server se movie ka Poster, Rating aur Year nikalega"""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    try:
        response = requests.get(url).json()
        if response.get("results"):
            best_match = response["results"][0]
            poster_path = best_match.get("poster_path")
            return {
                "poster": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
                "rating": round(best_match.get("vote_average", 7.4), 1),
                "year": best_match.get("release_date", "AI Pick").split("-")[0]
            }
    except Exception as e:
        print(f"Error fetching TMDB data for {movie_name}: {e}")
    return {"poster": None, "rating": "8.0", "year": "AI"}

# Home page check karne ke liye
@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running successfully! 🚀"}

# 🚀 NAYA ENDPOINT: VPN bypass wala (Trending movies ke liye)
@app.get("/trending")
def get_trending_movies():
    """Ye function bina VPN ke Render ke server se trending movies nikalega"""
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(url).json()
        return response.get("results", [])
    except Exception as e:
        return {"error": str(e)}

# Asli Recommendation wala API (Ab Posters aur Details ke saath)
@app.get("/recommend")
def recommend_movie(movie: str):
    try:
        # Thoda smart search kiya taaki CAPS ya small letters se error na aaye (.str.lower())
        movie_index = new_df[new_df['title'].str.lower() == movie.lower()].index[0]
        distances = similarity[movie_index]
        
        # Top 5 similar movies nikalna
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            movie_name = new_df.iloc[i[0]].title
            
            # Har recommended movie ka poster/rating backend me hi nikal rahe hain
            details = fetch_poster_and_details(movie_name)
            
            # Ab hum sirf naam nahi, balki poora data bhej rahe hain frontend ko
            recommended_movies.append({
                "name": movie_name,
                "poster": details["poster"],
                "rating": details["rating"],
                "year": details["year"]
            })
            
        return {
            "searched_movie": movie,
            "recommendations": recommended_movies
        }
        
    except IndexError:
        # Agar koi aisi movie dale jo database me nahi hai
        return {"error": f"Bhai, '{movie}' hamare database me nahi mili! Koi aur Hollywood movie ka naam try karo (Jaise: Avatar, Batman, Inception)."}
