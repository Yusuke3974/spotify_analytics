"""
FastAPI バックエンド - Spotify プレイリスト分析API
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from services.spotify_client import SpotifyService
from services.data_analyzer import DataAnalyzer
from services.db_service import save_analysis, get_latest_analysis, get_user_analysis_history
from core.database import get_db, init_db
from models.schemas import (
    PlaylistResponse,
    TrackResponse,
    AudioFeaturesResponse,
    PlaylistAnalysisResponse,
    GenreDistributionItem,
    MoodMapItem,
    TempoTrendsResponse,
    AnalysisHistoryResponse,
)

load_dotenv()

# データベース初期化（起動時）
init_db()

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


async def get_current_user_id(service: SpotifyService = Depends(get_spotify_service)) -> str:
    """現在のユーザーIDを取得"""
    try:
        me = service.get_current_user()
        return me["id"]
    except Exception:
        return "unknown"


@app.get("/")
async def root():
    return {"message": "Spotify Analytics API", "version": "1.0.0"}


@app.get("/api/playlists", response_model=List[PlaylistResponse])
async def get_playlists(service: SpotifyService = Depends(get_spotify_service)):
    """
    ユーザーのプレイリスト一覧を取得
    """
    try:
        playlists = await service.get_user_playlists()
        return playlists
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/playlist/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(
    playlist_id: str, service: SpotifyService = Depends(get_spotify_service)
):
    """
    プレイリストの詳細を取得
    """
    try:
        playlist = await service.get_playlist(playlist_id)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/playlist/{playlist_id}/analysis", response_model=PlaylistAnalysisResponse)
async def analyze_playlist(
    playlist_id: str, service: SpotifyService = Depends(get_spotify_service)
):
    """
    プレイリスト全体を分析
    """
    try:
        analysis = await service.analyze_playlist(playlist_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/genre-distribution", response_model=List[GenreDistributionItem])
async def get_genre_distribution(
    service: SpotifyService = Depends(get_spotify_service),
    db: Session = Depends(get_db),
    limit: int = 50,
    time_range: str = "medium_term",
    save: bool = True,
):
    """
    ジャンルの出現分布を返す

    Args:
        limit: 分析に使用する上位トラック数
        time_range: 期間 ("short_term", "medium_term", "long_term")
        save: DBに保存するかどうか（デフォルト: True）
    """
    try:
        user_id = await get_current_user_id(service)
        
        tracks_data = service.get_top_tracks_with_genres(
            limit=limit, time_range=time_range
        )
        distribution = DataAnalyzer.genre_distribution(tracks_data)
        
        # データベースに保存
        if save:
            save_analysis(
                db,
                user_id,
                "genre",
                time_range,
                {"distribution": [item.model_dump() if hasattr(item, "model_dump") else item for item in distribution]},
            )
        
        return distribution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/mood-map", response_model=List[MoodMapItem])
async def get_mood_map(
    service: SpotifyService = Depends(get_spotify_service),
    db: Session = Depends(get_db),
    limit: int = 50,
    time_range: str = "medium_term",
    save: bool = True,
):
    """
    valence × energy の散布図データを返す

    Args:
        limit: 分析に使用する上位トラック数
        time_range: 期間 ("short_term", "medium_term", "long_term")
        save: DBに保存するかどうか（デフォルト: True）
    """
    try:
        user_id = await get_current_user_id(service)
        
        tracks_data = service.get_user_top_tracks_with_features(
            limit=limit, time_range=time_range
        )
        mood_map = DataAnalyzer.mood_map(tracks_data)
        
        # データベースに保存
        if save:
            save_analysis(
                db,
                user_id,
                "mood",
                time_range,
                {"mood_map": [item.model_dump() if hasattr(item, "model_dump") else item for item in mood_map]},
            )
        
        return mood_map
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/tempo-trends", response_model=TempoTrendsResponse)
async def get_tempo_trends(
    service: SpotifyService = Depends(get_spotify_service),
    db: Session = Depends(get_db),
    limit: int = 50,
    time_range: str = "medium_term",
    save: bool = True,
):
    """
    テンポ（BPM）の平均・分布を返す

    Args:
        limit: 分析に使用する上位トラック数
        time_range: 期間 ("short_term", "medium_term", "long_term")
        save: DBに保存するかどうか（デフォルト: True）
    """
    try:
        user_id = await get_current_user_id(service)
        
        tracks_data = service.get_user_top_tracks_with_features(
            limit=limit, time_range=time_range
        )
        tempo_trends = DataAnalyzer.tempo_trends(tracks_data)
        
        # データベースに保存
        if save:
            save_analysis(
                db,
                user_id,
                "tempo",
                time_range,
                tempo_trends,
            )
        
        return tempo_trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/debug/raw-top-tracks")
async def get_raw_top_tracks(
    service: SpotifyService = Depends(get_spotify_service),
    limit: int = 20,
    time_range: str = "medium_term",
):
    """
    デバッグ用: Spotifyから取得した生データを返す

    Args:
        limit: 取得するトラック数
        time_range: 期間 ("short_term", "medium_term", "long_term")
    """
    try:
        tracks_data = service.get_top_tracks_with_genres(
            limit=limit, time_range=time_range
        )
        return {
            "count": len(tracks_data),
            "tracks": tracks_data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=List[AnalysisHistoryResponse])
async def get_history(
    service: SpotifyService = Depends(get_spotify_service),
    db: Session = Depends(get_db),
    analysis_type: Optional[str] = None,
    limit: int = 50,
):
    """
    ユーザーの分析履歴を取得

    Args:
        analysis_type: 分析タイプ（'genre', 'mood', 'tempo'、Noneの場合はすべて）
        limit: 取得件数
    """
    try:
        user_id = await get_current_user_id(service)
        
        history = get_user_analysis_history(
            db, user_id, analysis_type=analysis_type, limit=limit
        )
        
        # AnalysisHistoryをAnalysisHistoryResponseに変換
        result = [
            AnalysisHistoryResponse(
                id=item.id,
                user_id=item.user_id,
                analysis_type=item.analysis_type,
                time_range=item.time_range,
                result=item.result,
                created_at=item.created_at.isoformat(),
            )
            for item in history
        ]
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

