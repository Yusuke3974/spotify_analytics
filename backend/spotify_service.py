"""
Spotify API サービス - spotipyを使用したAPI連携
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Optional
import pandas as pd
import numpy as np

from backend.models import (
    PlaylistResponse,
    TrackResponse,
    AudioFeaturesResponse,
    PlaylistAnalysisResponse,
    PlaylistStats,
)


class SpotifyService:
    """Spotify APIとの連携を担当するサービス"""

    def __init__(self, access_token: str):
        """
        初期化
        
        Args:
            access_token: Spotify OAuthアクセストークン
        """
        self.client = spotipy.Spotify(auth=access_token)

    async def get_user_playlists(self) -> List[PlaylistResponse]:
        """ユーザーのプレイリスト一覧を取得"""
        playlists = []
        results = self.client.current_user_playlists(limit=50)

        while results:
            for item in results["items"]:
                playlists.append(
                    PlaylistResponse(
                        id=item["id"],
                        name=item["name"],
                        description=item.get("description"),
                        image_url=item["images"][0]["url"] if item["images"] else None,
                        track_count=item["tracks"]["total"],
                    )
                )
            if results["next"]:
                results = self.client.next(results)
            else:
                break

        return playlists

    async def get_playlist_details(self, playlist_id: str) -> PlaylistResponse:
        """プレイリストの詳細を取得"""
        playlist = self.client.playlist(playlist_id)

        return PlaylistResponse(
            id=playlist["id"],
            name=playlist["name"],
            description=playlist.get("description"),
            image_url=playlist["images"][0]["url"] if playlist["images"] else None,
            track_count=playlist["tracks"]["total"],
        )

    async def get_playlist_tracks(self, playlist_id: str) -> List[TrackResponse]:
        """プレイリストの曲一覧を取得"""
        tracks = []
        results = self.client.playlist_tracks(playlist_id, limit=50)

        while results:
            for item in results["items"]:
                if item["track"] and item["track"]["id"]:
                    track = item["track"]
                    tracks.append(
                        TrackResponse(
                            id=track["id"],
                            name=track["name"],
                            artists=[artist["name"] for artist in track["artists"]],
                            album_name=track["album"]["name"],
                            album_image=(
                                track["album"]["images"][0]["url"]
                                if track["album"]["images"]
                                else None
                            ),
                            duration_ms=track["duration_ms"],
                        )
                    )
            if results["next"]:
                results = self.client.next(results)
            else:
                break

        return tracks

    async def get_audio_features(self, track_id: str) -> AudioFeaturesResponse:
        """曲のオーディオ特徴を取得"""
        features = self.client.audio_features([track_id])[0]

        if not features:
            raise ValueError(f"Track {track_id} has no audio features")

        return AudioFeaturesResponse(
            id=features["id"],
            danceability=features["danceability"],
            energy=features["energy"],
            valence=features["valence"],
            tempo=features["tempo"],
            acousticness=features["acousticness"],
            instrumentalness=features["instrumentalness"],
            liveness=features["liveness"],
            speechiness=features["speechiness"],
            loudness=features["loudness"],
            mode=features["mode"],
            key=features["key"],
            time_signature=features["time_signature"],
        )

    async def get_audio_features_batch(
        self, track_ids: List[str]
    ) -> List[AudioFeaturesResponse]:
        """複数の曲のオーディオ特徴を一括取得"""
        features_list = []
        batch_size = 100

        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i : i + batch_size]
            features = self.client.audio_features(batch)

            for feature in features:
                if feature:
                    features_list.append(
                        AudioFeaturesResponse(
                            id=feature["id"],
                            danceability=feature["danceability"],
                            energy=feature["energy"],
                            valence=feature["valence"],
                            tempo=feature["tempo"],
                            acousticness=feature["acousticness"],
                            instrumentalness=feature["instrumentalness"],
                            liveness=feature["liveness"],
                            speechiness=feature["speechiness"],
                            loudness=feature["loudness"],
                            mode=feature["mode"],
                            key=feature["key"],
                            time_signature=feature["time_signature"],
                        )
                    )

        return features_list

    async def analyze_playlist(
        self, playlist_id: str
    ) -> PlaylistAnalysisResponse:
        """プレイリスト全体を分析"""
        # プレイリスト詳細を取得
        playlist = await self.get_playlist_details(playlist_id)

        # 曲一覧を取得
        tracks = await self.get_playlist_tracks(playlist_id)

        # 曲のIDを抽出
        track_ids = [track.id for track in tracks]

        # オーディオ特徴を取得
        features = await self.get_audio_features_batch(track_ids)

        # 統計情報を計算
        if features:
            df = pd.DataFrame([f.model_dump() for f in features])
            stats = PlaylistStats(
                total_tracks=len(tracks),
                analyzed_tracks=len(features),
                averages={
                    "danceability": float(df["danceability"].mean()),
                    "energy": float(df["energy"].mean()),
                    "valence": float(df["valence"].mean()),
                    "tempo": float(df["tempo"].mean()),
                    "acousticness": float(df["acousticness"].mean()),
                    "instrumentalness": float(df["instrumentalness"].mean()),
                    "liveness": float(df["liveness"].mean()),
                    "speechiness": float(df["speechiness"].mean()),
                },
                std_devs={
                    "danceability": float(df["danceability"].std()),
                    "energy": float(df["energy"].std()),
                    "valence": float(df["valence"].std()),
                    "tempo": float(df["tempo"].std()),
                    "acousticness": float(df["acousticness"].std()),
                    "instrumentalness": float(df["instrumentalness"].std()),
                    "liveness": float(df["liveness"].std()),
                    "speechiness": float(df["speechiness"].std()),
                },
            )
        else:
            stats = PlaylistStats(
                total_tracks=len(tracks),
                analyzed_tracks=0,
                averages={},
                std_devs={},
            )

        return PlaylistAnalysisResponse(
            playlist=playlist,
            tracks=tracks,
            features=features,
            stats=stats,
        )
