"""
プレイリストとトラックの取得（ページング対応）
実行: python -m scripts.fetch_playlists_and_tracks
"""

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from typing import List, Dict, Any

load_dotenv()

SCOPE = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=SCOPE,
        cache_path=".cache-spotify",
    ),
)


def paginate(func, key: str, limit: int = 50, **kwargs):
    """Spotifyのページングユーティリティ"""
    offset = 0
    items = []
    while True:
        result = func(limit=limit, offset=offset, **kwargs)
        items.extend(result[key]["items"])
        if result[key]["next"] is None:
            break
        offset += limit
    return items


# プレイリスト取得
playlists = paginate(sp.current_user_playlists, "playlists")

# トラック情報を集約
all_tracks = []

for playlist in playlists:
    playlist_id = playlist["id"]
    playlist_name = playlist["name"]
    playlist_tracks = paginate(
        sp.playlist_tracks, "items", playlist_id=playlist_id
    )

    for pt in playlist_tracks:
        if pt["track"] is None:
            continue
        track = pt["track"]
        if track["id"] is None:
            continue

        all_tracks.append(
            {
                "playlist_id": playlist_id,
                "playlist_name": playlist_name,
                "track_id": track["id"],
                "track_name": track["name"],
                "artists": ", ".join([a["name"] for a in track["artists"]]),
                "album_name": track["album"]["name"],
                "album_image": track["album"]["images"][0]["url"]
                if track["album"]["images"]
                else None,
                "duration_ms": track["duration_ms"],
            }
        )

# CSVに保存
df = pd.DataFrame(all_tracks)
df.to_csv("tracks_basic.csv", index=False, encoding="utf-8-sig")
print(f"✅ Saved {len(df)} tracks to tracks_basic.csv")

