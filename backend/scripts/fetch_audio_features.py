"""
オーディオ特徴量の取得（danceability, energy, tempo など）
実行: python -m scripts.fetch_audio_features
事前に tracks_basic.csv が必要です
"""

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from math import ceil

load_dotenv()

SCOPE = "user-top-read playlist-read-private playlist-read-collaborative user-library-read"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=SCOPE,
        cache_path=".cache-spotify",
    ),
)

# すでに作成済みのtracks_basic.csvを読み込み
tracks_df = pd.read_csv("tracks_basic.csv")
track_ids = tracks_df["track_id"].dropna().unique().tolist()

print(f"📊 Processing {len(track_ids)} tracks...")

# Spotify APIは一度に最大100曲まで取得可能
batch_size = 100
features_list = []

for i in range(0, len(track_ids), batch_size):
    batch = track_ids[i : i + batch_size]
    features = sp.audio_features(batch)
    features_list.extend([f for f in features if f is not None])
    print(f"  Processed {min(i + batch_size, len(track_ids))}/{len(track_ids)}")

# 特徴量をDataFrameに変換
features_df = pd.DataFrame(features_list)
features_df = features_df[
    [
        "id",
        "danceability",
        "energy",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness",
        "liveness",
        "speechiness",
        "loudness",
        "mode",
        "key",
        "time_signature",
    ]
]

# 元のデータと結合
merged_df = tracks_df.merge(
    features_df, left_on="track_id", right_on="id", how="left"
)
merged_df = merged_df.drop(columns=["id"])

# CSVに保存
merged_df.to_csv("tracks_with_features.csv", index=False, encoding="utf-8-sig")
print(f"✅ Saved {len(merged_df)} tracks with features to tracks_with_features.csv")

