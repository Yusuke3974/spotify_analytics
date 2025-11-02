"""
データベース操作サービス
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from core.database import AnalysisHistory


def save_analysis(
    db: Session,
    user_id: str,
    analysis_type: str,
    time_range: str,
    result: Dict[str, Any],
) -> AnalysisHistory:
    """
    分析結果をデータベースに保存

    Args:
        db: データベースセッション
        user_id: Spotify User ID
        analysis_type: 分析タイプ ('genre', 'mood', 'tempo')
        time_range: 期間 ('short_term', 'medium_term', 'long_term')
        result: 分析結果（JSON形式）

    Returns:
        保存されたAnalysisHistoryオブジェクト
    """
    analysis = AnalysisHistory(
        user_id=user_id,
        analysis_type=analysis_type,
        time_range=time_range,
        result=result,
        created_at=datetime.utcnow(),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_latest_analysis(
    db: Session,
    user_id: str,
    analysis_type: str,
    time_range: str,
) -> Optional[AnalysisHistory]:
    """
    最新の分析結果を取得

    Args:
        db: データベースセッション
        user_id: Spotify User ID
        analysis_type: 分析タイプ
        time_range: 期間

    Returns:
        最新のAnalysisHistoryオブジェクト、見つからない場合はNone
    """
    return (
        db.query(AnalysisHistory)
        .filter(
            AnalysisHistory.user_id == user_id,
            AnalysisHistory.analysis_type == analysis_type,
            AnalysisHistory.time_range == time_range,
        )
        .order_by(AnalysisHistory.created_at.desc())
        .first()
    )


def get_user_analysis_history(
    db: Session,
    user_id: str,
    analysis_type: Optional[str] = None,
    limit: int = 100,
) -> List[AnalysisHistory]:
    """
    ユーザーの分析履歴を取得

    Args:
        db: データベースセッション
        user_id: Spotify User ID
        analysis_type: 分析タイプ（Noneの場合はすべて）
        limit: 取得件数

    Returns:
        AnalysisHistoryオブジェクトのリスト
    """
    query = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == user_id)
    if analysis_type:
        query = query.filter(AnalysisHistory.analysis_type == analysis_type)
    return query.order_by(AnalysisHistory.created_at.desc()).limit(limit).all()

