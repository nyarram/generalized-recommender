# Game and Media Recommendation System

## Overview
This project is a recommendation system that fetches data from various APIs to provide users with personalized recommendations for games, movies, and music. It aims to deliver an engaging experience for entertainment seekers by leveraging data from popular platforms.

## Tech Stack
- **Languages**: Python
- **Libraries**: Requests, Pandas, Scikit-learn, Faiss
- **APIs**: Steam API, The Movie Database (TMDb) API, Spotify API

## Components
1. **Data Fetching Scripts**
   - `fetch_games.py`: Retrieves a list of games from the Steam API.
   - `fetch_movies.py`: Fetches movies from TMDb based on genre and popularity.
   - `fetch_music.py`: Gathers top tracks from Spotify based on genre.

2. **Recommendation System**
   - `recommend.py`: Merges data from movies, music, and games into a single dataset and provides recommendations using TF-IDF vectorization and similarity search.

3. **Data Storage**
   - `games.csv`, `movies.csv`, `music.csv`: Store the fetched data for easy access and analysis.
   - `top_RPG_games.csv`: Contains top-rated RPG games from the Steam API.

4. **User Access**
   - `test.py`: Demonstrates how to obtain a user access token from Spotify using the authorization code flow.

## Current Status
This project is a work in progress, focusing on refining the recommendation algorithms to provide the best possible suggestions.

## Upcoming Features/Improvements
- Enhanced recommendation algorithms for better accuracy.
- Building a user-friendly frontend for easier interaction.
- Integration of user feedback to improve recommendations.

## Installation
To run this project, install the required libraries:
```bash
pip install requests pandas scikit-learn faiss-cpu
```

## Usage
1. Fetch data by running:
   ```bash
   python fetch_games.py
   python fetch_movies.py
   python fetch_music.py
   ```
2. Get recommendations with:
   ```bash
   python recommend.py
   ```

## API Keys
Ensure to replace placeholder API keys in the scripts with your actual keys for Steam, TMDb, and Spotify.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Steam API](https://steamapi.com/)
- [The Movie Database (TMDb) API](https://developers.themoviedb.org/3)
- [Spotify API](https://developer.spotify.com/documentation/web-api/)