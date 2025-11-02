"""
最小スクリプト: Spotify認証 → 上位曲取得
実行: python -m scripts.auth_and_top_tracks
"""

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = "user-top-read"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=SCOPE,
        cache_path=".cache-spotify",  # トークンをローカルキャッシュ
        open_browser=True,  # 自動でブラウザ起動
    ),
)

me = sp.current_user()
print("✅ Authenticated as:", me["display_name"])

results = sp.current_user_top_tracks(limit=10, time_range="medium_term")
for i, item in enumerate(results["items"], start=1):
    artists = ", ".join(a["name"] for a in item["artists"])
    print(f"{i:2d}. {item['name']} — {artists}")

