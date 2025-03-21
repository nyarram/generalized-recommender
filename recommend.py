import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss  # Fast similarity search

# 🔹 Load datasets
movies_df = pd.read_csv("movies.csv")
music_df = pd.read_csv("music.csv")
games_df = pd.read_csv("games.csv")

# 🔹 Drop rows where name is NaN
games_df.dropna(subset=["name"], inplace=True)

# 🔹 Add type labels
movies_df["type"] = "movie"
music_df["type"] = "music"
games_df["type"] = "game"

# 🔹 Standardize column names
movies_df.rename(columns={"title": "name", "overview": "description"}, inplace=True)
music_df.rename(columns={"name": "name", "artist": "description"}, inplace=True)

# 🔹 Fix missing 'description' for games
if "description" not in games_df.columns:
    games_df["description"] = "No description available"

# 🔹 Fill missing descriptions
movies_df["description"] = movies_df["description"].fillna("No description available.")
music_df["description"] = music_df["description"].fillna("Unknown artist.")
games_df["description"] = games_df["description"].fillna("Unknown game.")

# 🔹 Convert all names to lowercase for consistent searching
movies_df["name"] = movies_df["name"].str.lower()
music_df["name"] = music_df["name"].str.lower()
games_df["name"] = games_df["name"].str.lower()

# 🔹 Merge into a single dataset
df = pd.concat([movies_df[["id", "name", "description", "type"]],
                music_df[["id", "name", "description", "type"]],
                games_df[["id", "name", "description", "type"]]])

df.reset_index(drop=True, inplace=True)

# 🔹 Remove rows where name is NaN
df.dropna(subset=["name"], inplace=True)

# 🔹 TF-IDF Vectorization with Optimization
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
tfidf_matrix = vectorizer.fit_transform(df["description"]).toarray()

# 🔹 Convert to Faiss Index
d = tfidf_matrix.shape[1]  # Dimensionality
index = faiss.IndexFlatL2(d)
index.add(tfidf_matrix)  # Add TF-IDF vectors to Faiss index

# 🔹 Function to Recommend Similar Items
def recommend_items(item_name, top_n=5):
    item_name = item_name.lower()  # Normalize input for search

    # 🔹 Use partial matching to find item
    matches = df[df["name"].str.contains(item_name, case=False, na=False, regex=False)]
    
    if matches.empty:
        print(f"❌ Item '{item_name}' not found. Available items: {df['name'].sample(5).tolist()}")
        return None

    item_idx = matches.index[0]
    query_vector = tfidf_matrix[item_idx].reshape(1, -1)

    # 🔹 Find top-N similar items using Faiss
    _, indices = index.search(query_vector, top_n + 1)  # +1 to exclude self
    indices = indices.flatten()[1:]  # Remove self from results
    
    recommendations = [{"name": df.iloc[i]["name"], "type": df.iloc[i]["type"]} for i in indices]

    return recommendations

# 🔹 Example Usage
if __name__ == "__main__":
    item = "Inception"  # Replace with any movie, song, or game
    recs = recommend_items(item, 10)
    
    if recs:
        print(f"\n🔹 Recommendations for '{item}':")
        for r in recs:
            print(f"- {r['name']} ({r['type']})")
