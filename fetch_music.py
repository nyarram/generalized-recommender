import requests
import pandas as pd

# Replace with your Spotify API credentials
CLIENT_ID = "f6a341872e3f41de83b89ec49ad8462d"
CLIENT_SECRET = "075e3e4c953e41a88fc46ff6036a6dbd"

# Spotify API URLs
AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1"

# 🔹 Function to get Spotify Access Token
def get_spotify_token():
    data = {"grant_type": "client_credentials"}
    auth = (CLIENT_ID, CLIENT_SECRET)
    
    response = requests.post(AUTH_URL, data=data, auth=auth)
    token_data = response.json()
    
    if response.status_code != 200:
        print(f"❌ Error getting token: {token_data}")
        return None

    return token_data["access_token"]

# 🔹 Function to fetch top tracks by searching a genre
def get_top_tracks(genre="rock", limit=50):
    token = get_spotify_token()
    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}"}
    
    # 🔹 Correct API endpoint: Search for top songs in a genre
    url = f"{BASE_URL}/search"
    params = {
        "q": f"genre:{genre}",  # Searching by genre
        "type": "track",
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error fetching tracks: {response.json()}")
        return None

    track_data = response.json()
    
    if "tracks" not in track_data:
        print("❌ No tracks found.")
        return None

    tracks = []
    for track in track_data["tracks"]["items"]:
        tracks.append({
            "id": track["id"],
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "popularity": track["popularity"],
            "preview_url": track.get("preview_url", ""),
            "genre": genre
        })
    
    return pd.DataFrame(tracks)

if __name__ == "__main__":
    df = get_top_tracks(genre="rap")  # You can change the genre here
    if df is not None:
        df.to_csv("music.csv", index=False)
        print("✅ Music data saved to music.csv")
    else:
        print("❌ No music data fetched.")
