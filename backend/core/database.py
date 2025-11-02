"""
データベース設定 - SQLAlchemy + SQLite
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from typing import Optional
import os

# SQLiteデータベースのパス
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./spotify_analytics.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite用
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class AnalysisHistory(Base):
    """分析履歴テーブル"""

    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # Spotify User ID
    analysis_type = Column(String, index=True)  # 'genre', 'mood', 'tempo'など
    time_range = Column(String)  # 'short_term', 'medium_term', 'long_term'
    result = Column(JSON)  # 分析結果をJSON形式で保存
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AnalysisHistory(id={self.id}, user_id={self.user_id}, type={self.analysis_type})>"


def get_db():
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """データベーステーブルを作成"""
    Base.metadata.create_all(bind=engine)

