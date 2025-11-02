"""
Pydanticモデル - APIリクエスト/レスポンスの型定義
"""

from pydantic import BaseModel
from typing import List, Optional, Dict


class TrackResponse(BaseModel):
    id: str
    name: str
    artists: List[str]
    album_name: str
    album_image: Optional[str]
    duration_ms: int


class AudioFeaturesResponse(BaseModel):
    id: str
    danceability: float
    energy: float
    valence: float
    tempo: float
    acousticness: float
    instrumentalness: float
    liveness: float
    speechiness: float
    loudness: float
    mode: int
    key: int
    time_signature: int


class PlaylistResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    track_count: int


class PlaylistStats(BaseModel):
    """プレイリストの統計情報"""
    total_tracks: int
    analyzed_tracks: int
    averages: Dict[str, float]
    std_devs: Dict[str, float]


class PlaylistAnalysisResponse(BaseModel):
    """プレイリスト分析結果"""
    playlist: PlaylistResponse
    tracks: List[TrackResponse]
    features: List[AudioFeaturesResponse]
    stats: PlaylistStats
