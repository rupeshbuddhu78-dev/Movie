from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

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

# Home page check karne ke liye
@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running successfully! 🚀"}

# Asli Recommendation wala API
@app.get("/recommend")
def recommend_movie(movie: str):
    try:
        # Movie ka index dhoondna
        movie_index = new_df[new_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        
        # Top 5 similar movies nikalna (1:6 kyunki index 0 pe wahi same movie hoti hai)
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(new_df.iloc[i[0]].title)
            
        return {
            "searched_movie": movie,
            "recommendations": recommended_movies
        }
        
    except IndexError:
        # Agar koi aisi movie dale jo database me nahi hai
        return {"error": f"Bhai, '{movie}' hamare database me nahi mili! Koi aur Hollywood movie ka naam try karo (Jaise: Avatar, Batman, Inception)."}from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

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

# Home page check karne ke liye
@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running successfully! 🚀"}

# Asli Recommendation wala API
@app.get("/recommend")
def recommend_movie(movie: str):
    try:
        # Movie ka index dhoondna
        movie_index = new_df[new_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        
        # Top 5 similar movies nikalna (1:6 kyunki index 0 pe wahi same movie hoti hai)
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(new_df.iloc[i[0]].title)
            
        return {
            "searched_movie": movie,
            "recommendations": recommended_movies
        }
        
    except IndexError:
        # Agar koi aisi movie dale jo database me nahi hai
        return {"error": f"Bhai, '{movie}' hamare database me nahi mili! Koi aur Hollywood movie ka naam try karo (Jaise: Avatar, Batman, Inception)."}