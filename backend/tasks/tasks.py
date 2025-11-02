"""
Celeryタスク - Spotifyデータの定期更新
"""

from tasks.celery_app import celery_app
from services.spotify_client import SpotifyService
from services.data_analyzer import DataAnalyzer
from services.db_service import save_analysis
from core.database import SessionLocal
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()


@celery_app.task(name="tasks.tasks.update_spotify_data")
def update_spotify_data():
    """
    定期更新タスク: 全ユーザーのSpotifyデータを更新
    
    注意: 実際の実装では、保存されているユーザートークンを使用して
    各ユーザーのデータを更新する必要があります。
    ここでは基本構造を示します。
    """
    try:
        # TODO: 保存されているユーザートークンのリストを取得
        # 今回はサンプル実装として、環境変数から直接取得
        # 実際の実装では、ユーザートークン管理テーブルから取得
        
        # データベースセッションを取得
        db = SessionLocal()
        
        try:
            # サンプル: 1ユーザーのデータを更新
            # 実際には、ユーザーリストをループして処理
            
            # ここでSpotifyOAuthを使用してトークンを取得
            # 実際の実装では、保存されているリフレッシュトークンを使用
            
            print("Spotify data update task executed")
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error in update_spotify_data task: {e}")
        raise


def update_user_analytics(
    user_id: str,
    access_token: str,
    time_range: str = "medium_term",
):
    """
    特定ユーザーの分析データを更新してDBに保存

    Args:
        user_id: Spotify User ID
        access_token: Spotify アクセストークン
        time_range: 期間
    """
    db = SessionLocal()
    try:
        service = SpotifyService(access_token)
        
        # ジャンル分布を取得して保存
        tracks_with_genres = service.get_top_tracks_with_genres(
            limit=50, time_range=time_range
        )
        genre_result = DataAnalyzer.genre_distribution(tracks_with_genres)
        save_analysis(
            db, user_id, "genre", time_range, {"distribution": genre_result}
        )
        
        # ムードマップを取得して保存
        tracks_with_features = service.get_user_top_tracks_with_features(
            limit=50, time_range=time_range
        )
        mood_result = DataAnalyzer.mood_map(tracks_with_features)
        save_analysis(
            db, user_id, "mood", time_range, {"mood_map": mood_result}
        )
        
        # テンポトレンドを取得して保存
        tempo_result = DataAnalyzer.tempo_trends(tracks_with_features)
        save_analysis(
            db, user_id, "tempo", time_range, tempo_result
        )
        
        db.commit()
        print(f"Updated analytics for user {user_id}")
        
    except Exception as e:
        db.rollback()
        print(f"Error updating analytics for user {user_id}: {e}")
        raise
    finally:
        db.close()

