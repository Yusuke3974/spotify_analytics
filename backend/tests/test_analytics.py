"""
/analytics系APIのテスト
pytest + HTTPX使用
"""

import pytest
from httpx import AsyncClient
import sys
from pathlib import Path

# backendディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app
from unittest.mock import Mock, patch


@pytest.fixture
async def client():
    """テスト用のクライアント"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_spotify_service():
    """SpotifyServiceのモック"""
    mock_service = Mock()
    
    # モックデータ
    mock_tracks_with_genres = [
        {
            "track": "Test Song 1",
            "track_id": "track1",
            "genres": ["pop", "rock"],
            "valence": 0.75,
            "energy": 0.85,
            "tempo": 120.0,
        },
        {
            "track": "Test Song 2",
            "track_id": "track2",
            "genres": ["pop", "j-pop"],
            "valence": 0.65,
            "energy": 0.70,
            "tempo": 130.0,
        },
    ]
    
    mock_tracks_with_features = [
        {
            "track": "Test Song 1",
            "track_id": "track1",
            "valence": 0.75,
            "energy": 0.85,
            "tempo": 120.0,
        },
        {
            "track": "Test Song 2",
            "track_id": "track2",
            "valence": 0.65,
            "energy": 0.70,
            "tempo": 130.0,
        },
    ]
    
    async def get_top_tracks_with_genres(limit=50, time_range="medium_term"):
        return mock_tracks_with_genres
    
    async def get_user_top_tracks_with_features(limit=50, time_range="medium_term"):
        return mock_tracks_with_features
    
    mock_service.get_top_tracks_with_genres = get_top_tracks_with_genres
    mock_service.get_user_top_tracks_with_features = get_user_top_tracks_with_features
    mock_service.client = Mock()
    mock_service.client.current_user.return_value = {"id": "test_user_id"}
    
    return mock_service


@pytest.mark.asyncio
async def test_genre_distribution(client: AsyncClient, mock_spotify_service):
    """ジャンル分布APIのテスト"""
        from core.database import SessionLocal
    
    async def mock_get_current_user_id(*args, **kwargs):
        return "test_user_id"
    
    with patch("api.main.get_spotify_service", return_value=mock_spotify_service), \
         patch("api.main.get_current_user_id", side_effect=mock_get_current_user_id), \
         patch("core.database.get_db") as mock_get_db:
        mock_db = SessionLocal()
        async def mock_db_gen():
            try:
                yield mock_db
            finally:
                mock_db.close()
        mock_get_db.return_value = mock_db_gen()
        
        response = await client.get(
            "/analytics/genre-distribution?limit=50&time_range=medium_term&save=false",
            headers={"Authorization": "Bearer test_token"},
        )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "genre" in data[0]
        assert "count" in data[0]


@pytest.mark.asyncio
async def test_mood_map(client: AsyncClient, mock_spotify_service):
    """ムードマップAPIのテスト"""
        from core.database import SessionLocal
    
    async def mock_get_current_user_id(*args, **kwargs):
        return "test_user_id"
    
    with patch("api.main.get_spotify_service", return_value=mock_spotify_service), \
         patch("api.main.get_current_user_id", side_effect=mock_get_current_user_id), \
         patch("core.database.get_db") as mock_get_db:
        mock_db = SessionLocal()
        async def mock_db_gen():
            try:
                yield mock_db
            finally:
                mock_db.close()
        mock_get_db.return_value = mock_db_gen()
        
        response = await client.get(
            "/analytics/mood-map?limit=50&time_range=medium_term&save=false",
            headers={"Authorization": "Bearer test_token"},
        )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "track" in data[0]
        assert "valence" in data[0]
        assert "energy" in data[0]


@pytest.mark.asyncio
async def test_tempo_trends(client: AsyncClient, mock_spotify_service):
    """テンポトレンドAPIのテスト"""
        from core.database import SessionLocal
    
    async def mock_get_current_user_id(*args, **kwargs):
        return "test_user_id"
    
    with patch("api.main.get_spotify_service", return_value=mock_spotify_service), \
         patch("api.main.get_current_user_id", side_effect=mock_get_current_user_id), \
         patch("core.database.get_db") as mock_get_db:
        mock_db = SessionLocal()
        async def mock_db_gen():
            try:
                yield mock_db
            finally:
                mock_db.close()
        mock_get_db.return_value = mock_db_gen()
        
        response = await client.get(
            "/analytics/tempo-trends?limit=50&time_range=medium_term&save=false",
            headers={"Authorization": "Bearer test_token"},
        )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "mean_tempo" in data
    assert "std_tempo" in data
    assert "distribution" in data
    assert isinstance(data["distribution"], list)


@pytest.mark.asyncio
async def test_debug_raw_top_tracks(client: AsyncClient, mock_spotify_service):
    """デバッグエンドポイントのテスト"""
    with patch("api.main.get_spotify_service", return_value=mock_spotify_service):
        response = await client.get(
            "/debug/raw-top-tracks?limit=20&time_range=medium_term",
            headers={"Authorization": "Bearer test_token"},
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "tracks" in data
    assert isinstance(data["tracks"], list)

