"""
データ分析処理 - pandasで分析処理
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class DataAnalyzer:
    """プレイリストデータの分析を行うクラス"""

    def __init__(self, features_df: pd.DataFrame):
        """
        初期化

        Args:
            features_df: オーディオ特徴量を含むDataFrame
        """
        self.features_df = features_df.copy()

    def calculate_statistics(self) -> Dict[str, Any]:
        """
        基本統計量を計算

        Returns:
            統計情報の辞書
        """
        numeric_cols = [
            "danceability",
            "energy",
            "valence",
            "tempo",
            "acousticness",
            "instrumentalness",
            "liveness",
            "speechiness",
        ]

        stats = {}
        for col in numeric_cols:
            if col in self.features_df.columns:
                stats[f"{col}_mean"] = float(self.features_df[col].mean())
                stats[f"{col}_std"] = float(self.features_df[col].std())
                stats[f"{col}_min"] = float(self.features_df[col].min())
                stats[f"{col}_max"] = float(self.features_df[col].max())

        return stats

    def cluster_tracks(
        self, n_clusters: int = 5, features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        k-meansクラスタリングでトラックを分類

        Args:
            n_clusters: クラスタ数
            features: 使用する特徴量（Noneの場合は主要な特徴量を使用）

        Returns:
            クラスタラベルが追加されたDataFrame
        """
        if features is None:
            features = [
                "danceability",
                "energy",
                "valence",
                "acousticness",
                "instrumentalness",
            ]

        # 使用可能な特徴量のみを選択
        available_features = [f for f in features if f in self.features_df.columns]
        if len(available_features) == 0:
            raise ValueError("使用可能な特徴量が見つかりません")

        # 特徴量を抽出
        X = self.features_df[available_features].values

        # NaNを処理
        X = np.nan_to_num(X, nan=0.0)

        # 標準化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # k-meansクラスタリング
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        # 結果をDataFrameに追加
        result_df = self.features_df.copy()
        result_df["cluster"] = labels

        return result_df

    def get_cluster_characteristics(self, clustered_df: pd.DataFrame) -> Dict[int, Dict[str, float]]:
        """
        各クラスタの特徴を計算

        Args:
            clustered_df: クラスタリング済みのDataFrame

        Returns:
            クラスタIDをキーとした特徴量の辞書
        """
        characteristics = {}
        numeric_cols = [
            "danceability",
            "energy",
            "valence",
            "acousticness",
            "instrumentalness",
        ]

        for cluster_id in clustered_df["cluster"].unique():
            cluster_data = clustered_df[clustered_df["cluster"] == cluster_id]
            char = {}
            for col in numeric_cols:
                if col in cluster_data.columns:
                    char[col] = float(cluster_data[col].mean())
            characteristics[int(cluster_id)] = char

        return characteristics

    def get_representative_tracks(
        self, clustered_df: pd.DataFrame, n_tracks: int = 3
    ) -> Dict[int, List[str]]:
        """
        各クラスタの代表曲を取得（クラスタの中心に近い曲）

        Args:
            clustered_df: クラスタリング済みのDataFrame
            n_tracks: 各クラスタから取得する曲数

        Returns:
            クラスタIDをキーとした代表曲のIDリストの辞書
        """
        representative_tracks = {}
        numeric_cols = [
            "danceability",
            "energy",
            "valence",
            "acousticness",
            "instrumentalness",
        ]
        available_features = [f for f in numeric_cols if f in clustered_df.columns]

        for cluster_id in clustered_df["cluster"].unique():
            cluster_data = clustered_df[clustered_df["cluster"] == cluster_id]

            # クラスタの中心を計算
            cluster_center = cluster_data[available_features].mean().values

            # 各曲とクラスタ中心の距離を計算
            distances = []
            for idx, row in cluster_data.iterrows():
                track_features = row[available_features].values
                distance = np.linalg.norm(track_features - cluster_center)
                distances.append((idx, distance))

            # 距離が小さい順にソート
            distances.sort(key=lambda x: x[1])

            # 代表曲を取得
            track_ids = []
            for idx, _ in distances[:n_tracks]:
                if "track_id" in clustered_df.columns:
                    track_ids.append(clustered_df.loc[idx, "track_id"])
            
            representative_tracks[int(cluster_id)] = track_ids

        return representative_tracks

    @staticmethod
    def genre_distribution(
        tracks_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        ジャンルの出現分布を分析

        Args:
            tracks_data: トラック情報のリスト（各要素は{"genres": List[str], ...}を含む）

        Returns:
            [{genre: str, count: int}] の形式のリスト
        """
        genre_counts = {}
        for track in tracks_data:
            genres = track.get("genres", [])
            if not isinstance(genres, list):
                continue
            for genre in genres:
                if genre:  # Noneや空文字列をスキップ
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1

        result = [
            {"genre": genre, "count": count}
            for genre, count in genre_counts.items()
        ]
        result.sort(key=lambda x: x["count"], reverse=True)
        return result

    @staticmethod
    def mood_map(
        tracks_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        valence × energy の散布図データを分析

        Args:
            tracks_data: トラック情報のリスト（各要素は{"track": str, "valence": float, "energy": float}を含む）

        Returns:
            [{track: str, valence: float, energy: float}] の形式のリスト
        """
        result = []
        for track in tracks_data:
            track_name = track.get("track", track.get("name", "Unknown"))
            valence = track.get("valence")
            energy = track.get("energy")

            # None値をスキップ
            if valence is not None and energy is not None:
                result.append(
                    {
                        "track": track_name,
                        "valence": float(valence),
                        "energy": float(energy),
                    }
                )

        return result

    @staticmethod
    def tempo_trends(
        tracks_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        テンポ（BPM）の平均・分布を分析

        Args:
            tracks_data: トラック情報のリスト（各要素は{"tempo": float}を含む）

        Returns:
            {
                "mean_tempo": float,
                "std_tempo": float,
                "distribution": [{"range": str, "count": int}]
            }
        """
        tempos = []
        for track in tracks_data:
            tempo = track.get("tempo")
            if tempo is not None:
                tempos.append(float(tempo))

        if not tempos:
            return {
                "mean_tempo": 0.0,
                "std_tempo": 0.0,
                "distribution": [],
            }

        df = pd.DataFrame({"tempo": tempos})
        mean_tempo = float(df["tempo"].mean())
        std_tempo = float(df["tempo"].std())

        # テンポの分布を20のビンに分割
        bins = [0, 60, 80, 100, 120, 140, 160, 180, 200, 220, float("inf")]
        labels = [
            "0-60",
            "60-80",
            "80-100",
            "100-120",
            "120-140",
            "140-160",
            "160-180",
            "180-200",
            "200-220",
            "220+",
        ]

        df["range"] = pd.cut(
            df["tempo"], bins=bins, labels=labels, include_lowest=True
        )
        distribution_counts = df["range"].value_counts().sort_index()

        distribution = [
            {"range": str(range_label), "count": int(count)}
            for range_label, count in distribution_counts.items()
        ]

        return {
            "mean_tempo": mean_tempo,
            "std_tempo": std_tempo,
            "distribution": distribution,
        }

