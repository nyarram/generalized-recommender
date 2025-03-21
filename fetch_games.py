import requests
import pandas as pd

# 🔹 Your Steam API Key
STEAM_API_KEY = "92023E32787EFEE60B56314BD3D25CC2"

# 🔹 API Endpoints
APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
DETAILS_URL = "https://store.steampowered.com/api/appdetails?appids={game_id}"
REVIEWS_URL = "https://store.steampowered.com/appreviews/{game_id}?json=1"

# 🔹 SteamSpy API (Publicly available game statistics)
STEAMSPY_API_URL = "https://steamspy.com/api.php"

# 🔹 Steam Storefront API to Fetch Top Games by Genre
STEAM_STORE_URL = "https://store.steampowered.com/api/featuredcategories/"

# 🔹 Function to Fetch All Games
def get_steam_games(limit=100):
    response = requests.get(APP_LIST_URL)
    
    if response.status_code != 200:
        print(f"❌ Error fetching game list: {response.json()}")
        return None
    
    game_data = response.json()
    
    if "applist" not in game_data or "apps" not in game_data["applist"]:
        print("❌ No games found.")
        return None

    # 🔹 Extract game ID & name, filtering out empty names
    games = [{"id": game["appid"], "name": game["name"]} for game in game_data["applist"]["apps"] if game["name"].strip()]

    # 🔹 Limit the number of games if a limit is provided
    if limit is not None:
        games = games[:limit]

    return games

# 🔹 Function to Fetch Game Details by Genre & Rating
# def get_top_rated_games(genre, limit=10):
#     all_games = get_steam_games(limit=500)  # Fetch a larger list to filter from
#     if not all_games:
#         return None
    
#     matching_games = []
    
#     for game in all_games:
#         details_url = DETAILS_URL.format(game_id=game["id"])
#         response = requests.get(details_url)
        
#         if response.status_code != 200:
#             continue
        
#         data = response.json()
        
#         if str(game["id"]) not in data or not data[str(game["id"])] or not data[str(game["id"])] ["success"]:
#             continue
        
#         game_info = data[str(game["id"])]["data"]
        
#         if "genres" in game_info:
#             game_genres = [g["description"].lower() for g in game_info["genres"]]
            
#             if genre.lower() in game_genres:
#                 # 🔹 Fetch review scores
#                 review_response = requests.get(REVIEWS_URL.format(game_id=game["id"]))
#                 review_score = 0
#                 total_reviews = 0
                
#                 if review_response.status_code == 200:
#                     review_data = review_response.json()
#                     review_score = review_data.get("query_summary", {}).get("review_score", 0)
#                     total_reviews = review_data.get("query_summary", {}).get("total_reviews", 0)
                
#                 matching_games.append({
#                     "id": game["id"],
#                     "name": game["name"],
#                     "genres": game_genres,
#                     "price": game_info.get("price_overview", {}).get("final_formatted", "Free"),
#                     "release_date": game_info.get("release_date", {}).get("date", "Unknown"),
#                     "steam_url": f"https://store.steampowered.com/app/{game['id']}",
#                     "review_score": review_score,
#                     "total_reviews": total_reviews
#                 })
        
#     # 🔹 Sort by highest review score & most reviews
#     matching_games.sort(key=lambda x: (-x["review_score"], -x["total_reviews"]))
    
#     return pd.DataFrame(matching_games[:limit])

# 🔹 Function to Fetch Top-Rated Games by Genre
def get_top_rated_games(genre, limit=10):
    response = requests.get(STEAM_STORE_URL)
    
    if response.status_code != 200:
        print(f"❌ Error fetching data: HTTP {response.status_code}")
        return None
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ Error: Received an invalid JSON response from Steam.")
        return None
    
    games = []
    
    # 🔹 Extract games from featured categories (bestsellers, new releases, etc.)
    for category in data.get("featured_win", []):
        for game in category.get("items", []):
            if genre.lower() in [g.lower() for g in game.get("genres", [])]:
                games.append({
                    "id": game.get("id", "N/A"),
                    "name": game.get("name", "Unknown"),
                    "price": game.get("price", {}).get("final_formatted", "Free"),
                    "release_date": game.get("release_date", {}).get("date", "Unknown"),
                    "review_score": game.get("review_summary", {}).get("score", 0),
                    "total_reviews": game.get("review_summary", {}).get("total_reviews", 0),
                    "steam_url": f"https://store.steampowered.com/app/{game.get('id', 'N/A')}"
                })
    
    # 🔹 Sort by highest review score and total reviews
    games.sort(key=lambda x: (-x["review_score"], -x["total_reviews"]))
    
    return pd.DataFrame(games[:limit])

if __name__ == "__main__":
    genre = "RPG"  # Change this to your preferred genre (e.g., "Action", "Strategy")
    df = get_top_rated_games(genre, limit=10)
    if df is not None:
        df.to_csv(f"top_{genre}_games.csv", index=False)
        print(f"✅ Top-rated {genre} games saved to top_{genre}_games.csv")
    else:
        print("❌ No matching games found.")