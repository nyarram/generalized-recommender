import requests
import pandas as pd

API_KEY = "f77580ffddb080e9cd5f3e2007bbd192"
BASE_URL = "https://api.themoviedb.org/3"

# Function to fetch movies by genre
def get_movies(genre_id=28, num_pages=3):  # 28 = Action (Default)
    movies = []
    
    for page in range(1, num_pages+1):
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "include_video": "false",
            "page": page,
            "with_genres": genre_id
        }
        
        response = requests.get(url, params=params).json()
        
        if "results" not in response:
            print(f"❌ Error: {response}")  # Debugging
            return None

        for movie in response["results"]:
            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie.get("overview", ""),
                "popularity": movie["popularity"],
                "release_date": movie["release_date"],
                "vote_average": movie["vote_average"]
            })
    
    return pd.DataFrame(movies)

if __name__ == "__main__":
    df = get_movies()
    if df is not None:
        df.to_csv("movies.csv", index=False)
        print("✅ Movies saved to movies.csv")
    else:
        print("❌ No movies fetched. Check API key or request.")
