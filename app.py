import os
import uuid
from flask import Flask, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = '7986b71639264f29885584c048651e05'
CLIENT_SECRET = '1aa0b427c20d444db3a1fc7140e08ab6'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-library-read user-top-read'

def create_spotify_oauth():
    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())
    cache_path = f".cache-{session['uuid']}"
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=cache_path,
        show_dialog=True  # FORCE login screen
    )

@app.route('/')
def login():
    session.clear()  # Clear session on home load
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return f'''
    <html>
    <head>
        <title>Spotify Login</title>
    </head>
    <body style="background:#191414;color:white;text-align:center;font-family:sans-serif;">
        <h2>Login with Spotify</h2>
        <a href="{auth_url}" style="padding:12px 24px;background:#1DB954;color:white;border-radius:30px;text-decoration:none;">Login</a>
    </body>
    </html>
    '''

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    if not code:
        return "Authorization failed", 400
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('top_tracks'))

@app.route('/top-tracks')
def top_tracks():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_top_tracks(limit=10, time_range='long_term')
    tracks = results['items']

    html_tracks = ''.join(f'<li>{track["name"]} by {track["artists"][0]["name"]}</li>' for track in tracks)

    return f'''
    <html>
    <head><title>Top Tracks</title></head>
    <body style="background:#191414;color:white;font-family:sans-serif;padding:40px;">
        <h2 style="color:#1DB954;">Your Top 10 Tracks</h2>
        <ol>{html_tracks}</ol>
        <a href="/logout" style="display:block;margin-top:30px;text-align:center;color:#1DB954;">Logout / Switch User</a>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    if 'uuid' in session:
        cache_path = f".cache-{session['uuid']}"
        if os.path.exists(cache_path):
            os.remove(cache_path)
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
