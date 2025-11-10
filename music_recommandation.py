
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Debug: Verify credentials
if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
    print("Error: One or more environment variables are missing in .env file")
    exit()

# Authenticate with Spotify
scope = "user-library-read user-top-read playlist-modify-public"
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                  client_secret=SPOTIPY_CLIENT_SECRET,
                                                  redirect_uri=SPOTIPY_REDIRECT_URI,
                                                  scope=scope))
    # Test authentication
    user = sp.current_user()
    print(f"Authenticated as: {user['display_name']}")
except spotipy.exceptions.SpotifyOauthError as e:
    print(f"Authentication error: {e}")
    exit()

# Fetch user's top tracks
try:
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')
    tracks = top_tracks['items']
    if not tracks:
        print("No top tracks found. Please listen to more music on Spotify.")
        exit()
    track_data = []
    for track in tracks:
        track_data.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name']
        })

    # Fetch audio features
    track_ids = [track['id'] for track in track_data]
    audio_features = sp.audio_features(track_ids)
    for i, feature in enumerate(audio_features):
        if feature:  # Ensure feature is not None
            track_data[i].update({
                'danceability': feature['danceability'],
                'energy': feature['energy'],
                'tempo': feature['tempo'],
                'valence': feature['valence'],
                'acousticness': feature['acousticness']
            })

    # Save to DataFrame
    df_user_tracks = pd.DataFrame(track_data)
    df_user_tracks.to_csv('user_tracks.csv', index=False)
    print("User tracks saved to user_tracks.csv")
except spotipy.exceptions.SpotifyException as e:
    print(f"Error fetching user tracks: {e}")
    exit()

# Preprocess data
features = ['danceability', 'energy', 'tempo', 'valence', 'acousticness']
X = df_user_tracks[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Compute similarity
similarity_matrix = cosine_similarity(X_scaled)

# Recommend tracks from user's history
def recommend_tracks(track_index, num_recommendations=5):
    sim_scores = list(enumerate(similarity_matrix[track_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
    return df_user_tracks.iloc[top_indices][['name', 'artist']]

# Print recommendations from user history
print("\nRecommended Tracks (from user history):")
print(recommend_tracks(0))

# Fetch new tracks from a playlist
try:
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'  # Today's Top Hits
    playlist_tracks = sp.playlist_tracks(playlist_id)['items']
    new_tracks = []
    for item in playlist_tracks:
        track = item['track']
        if track:  # Ensure track is not None
            new_tracks.append({
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name']
            })

    # Fetch audio features for new tracks
    new_track_ids = [track['id'] for track in new_tracks]
    new_audio_features = sp.audio_features(new_track_ids)
    for i, feature in enumerate(new_audio_features):
        if feature:  # Ensure feature is not None
            new_tracks[i].update({
                'danceability': feature['danceability'],
                'energy': feature['energy'],
                'tempo': feature['tempo'],
                'valence': feature['valence'],
                'acousticness': feature['acousticness']
            })

    df_new_tracks = pd.DataFrame(new_tracks)
except spotipy.exceptions.SpotifyException as e:
    print(f"Error fetching playlist tracks: {e}")
    exit()

# Combine user and new tracks
df_all = pd.concat([df_user_tracks, df_new_tracks], ignore_index=True)

# Normalize combined features
X_all = df_all[features]
X_all_scaled = scaler.fit_transform(X_all)

# Compute similarity between user tracks and all tracks
similarity_matrix_all = cosine_similarity(X_all_scaled[:len(df_user_tracks)], X_all_scaled)

# Recommend new tracks
def recommend_new_tracks(num_recommendations=5):
    sim_scores = similarity_matrix_all.mean(axis=0)
    top_indices = sim_scores.argsort()[-num_recommendations-1:-1][::-1]
    return df_all.iloc[top_indices][['name', 'artist']], top_indices

# Print new track recommendations
print("\nNew Track Recommendations:")
recommendations, top_indices = recommend_new_tracks()
print(recommendations)

# Create a playlist
try:
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, "AI Recommendations", public=True)
    playlist_id = playlist['id']
    recommended_track_ids = df_all.iloc[top_indices]['id'].tolist()
    sp.playlist_add_items(playlist_id, recommended_track_ids)
    print(f"\nPlaylist created: {playlist['external_urls']['spotify']}")
except spotipy.exceptions.SpotifyException as e:
    print(f"Error creating playlist: {e}")
