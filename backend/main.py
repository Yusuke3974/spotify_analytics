"""
FastAPI バックエンド - Spotify プレイリスト分析API
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import os
from dotenv import load_dotenv

from backend.spotify_service import SpotifyService
from backend.models import (
    PlaylistResponse,
    TrackResponse,
    AudioFeaturesResponse,
    PlaylistAnalysisResponse,
)

load_dotenv()

app = FastAPI(title="Spotify Analytics API", version="1.0.0")

# CORS設定（Streamlitからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に設定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


def get_spotify_service(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """認証トークンからSpotifyServiceを取得"""
    token = credentials.credentials
    return SpotifyService(token)


@app.get("/")
async def root():
    return {"message": "Spotify Analytics API", "version": "1.0.0"}


@app.get("/api/playlists", response_model=List[PlaylistResponse])
async def get_playlists(service: SpotifyService = Depends(get_spotify_service)):
    """ユーザーのプレイリスト一覧を取得"""
    try:
        playlists = await service.get_user_playlists()
        return playlists
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/playlist/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(
    playlist_id: str, service: SpotifyService = Depends(get_spotify_service)
):
    """プレイリストの詳細を取得"""
    try:
        playlist = await service.get_playlist_details(playlist_id)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/playlist/{playlist_id}/tracks", response_model=List[TrackResponse])
async def get_playlist_tracks(
    playlist_id: str, service: SpotifyService = Depends(get_spotify_service)
):
    """プレイリストの曲一覧を取得"""
    try:
        tracks = await service.get_playlist_tracks(playlist_id)
        return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/audio-features/{track_id}", response_model=AudioFeaturesResponse)
async def get_audio_features(
    track_id: str, service: SpotifyService = Depends(get_spotify_service)
):
    """曲のオーディオ特徴を取得"""
    try:
        features = await service.get_audio_features(track_id)
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/playlist/{playlist_id}/analysis", response_model=PlaylistAnalysisResponse)
async def analyze_playlist(
    playlist_id: str, service: SpotifyService = Depends(get_spotify_service)
):
    """プレイリスト全体を分析"""
    try:
        analysis = await service.analyze_playlist(playlist_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
