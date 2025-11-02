# 🎵 Spotify Analytics Backend

FastAPIベースのSpotify分析バックエンドAPI

## 📋 概要

このバックエンドは、Spotify APIを使用してユーザーの音楽データを取得・分析し、分析結果を可視化するためのRESTful APIを提供します。

## 🏗️ プロジェクト構造

```
backend/
├── api/                      # FastAPIアプリケーション
│   ├── __init__.py
│   └── main.py               # FastAPIエントリポイント
├── core/                      # コア設定
│   ├── __init__.py
│   ├── config.py             # 設定管理
│   └── database.py           # SQLAlchemy設定とDBモデル
├── models/                    # データモデル
│   ├── __init__.py
│   └── schemas.py            # Pydanticモデル（APIレスポンス定義）
├── services/                   # ビジネスロジック層
│   ├── __init__.py
│   ├── spotify_client.py     # SpotipyでSpotify API呼び出し
│   ├── data_analyzer.py      # pandasで分析処理
│   └── db_service.py          # データベース操作サービス
├── tasks/                     # Celeryタスク
│   ├── __init__.py
│   ├── celery_app.py         # Celery設定
│   └── tasks.py               # Celeryタスク（定期更新）
├── scripts/                   # データ取得スクリプト
│   ├── __init__.py
│   ├── auth_and_top_tracks.py      # 最小スクリプト（ログイン→上位曲）
│   ├── fetch_playlists_and_tracks.py # プレイリストとトラック取得
│   └── fetch_audio_features.py      # オーディオ特徴量取得
├── tests/                     # テストコード
│   ├── __init__.py
│   └── test_analytics.py     # pytest + HTTPXテスト
├── pyproject.toml            # Python依存関係（uv使用）
├── pytest.ini                 # pytest設定
└── README.md                  # このファイル
```

## 🚀 機能

### 1. プレイリスト分析API
- `/api/playlists`: ユーザーのプレイリスト一覧を取得
- `/api/playlist/{playlist_id}`: プレイリスト詳細を取得
- `/api/playlist/{playlist_id}/analysis`: プレイリスト全体を分析

### 2. ユーザー分析API
- `/analytics/genre-distribution`: ジャンルの出現分布を返す
- `/analytics/mood-map`: valence × energy の散布図データを返す
- `/analytics/tempo-trends`: テンポ（BPM）の平均・分布を返す

### 3. 分析履歴API
- `/history`: ユーザーの分析履歴を取得（DBに保存された結果）

### 4. デバッグAPI
- `/debug/raw-top-tracks`: Spotifyから取得した生データを返す

## 🔧 セットアップ

### 前提条件

- Python 3.10以上
- [uv](https://github.com/astral-sh/uv) (Pythonパッケージ管理ツール)

### 1. 依存関係のインストール

```bash
cd backend
uv sync
```

### 2. 環境変数の設定

`.env`ファイルを作成し、以下の環境変数を設定してください：

```env
# Spotify API設定
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:3000

# データベース設定（オプション）
DATABASE_URL=sqlite:///./spotify_analytics.db

# Redis設定（Celery用、オプション）
REDIS_URL=redis://localhost:6379/0
```

### 3. データベースの初期化

データベースは自動的に作成されます。初回起動時に`core/database.py`の`init_db()`が実行されます。

手動で初期化する場合：

```bash
uv run python -c "from core.database import init_db; init_db()"
```

## 🚀 起動方法

### 開発サーバーの起動

```bash
cd backend
uv run uvicorn api.main:app --reload --port 8000
```

### APIドキュメントの確認

起動後、以下のURLでAPIドキュメント（Swagger UI）を確認できます：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 使用方法

### 認証

すべてのAPIエンドポイントはBearerトークン認証を使用します。

```bash
curl -X GET "http://localhost:8000/api/playlists" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 分析APIの使用例

#### ジャンル分布の取得

```bash
curl -X GET "http://localhost:8000/analytics/genre-distribution?limit=50&time_range=medium_term" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### ムードマップの取得

```bash
curl -X GET "http://localhost:8000/analytics/mood-map?limit=50&time_range=medium_term" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### テンポトレンドの取得

```bash
curl -X GET "http://localhost:8000/analytics/tempo-trends?limit=50&time_range=medium_term" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 分析履歴の取得

```bash
curl -X GET "http://localhost:8000/history?limit=50&analysis_type=tempo" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🗄️ データベース

### SQLiteデータベース

デフォルトではSQLiteデータベース（`spotify_analytics.db`）を使用します。

### テーブル構造

#### `analysis_history`

分析履歴を保存するテーブル。

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | Integer | プライマリキー |
| user_id | String | Spotify User ID |
| analysis_type | String | 分析タイプ（'genre', 'mood', 'tempo'） |
| time_range | String | 期間（'short_term', 'medium_term', 'long_term'） |
| result | JSON | 分析結果（JSON形式） |
| created_at | DateTime | 作成日時 |

## 🔄 Celery + Redis（定期更新）

### 1. Redisの起動

```bash
# Dockerを使用する場合
docker run -d -p 6379:6379 redis:latest

# または、ローカルにRedisがインストールされている場合
redis-server
```

### 2. Celery Workerの起動

```bash
cd backend
uv run celery -A tasks.celery_app worker --loglevel=info
```

### 3. Celery Beat（スケジューラー）の起動

```bash
cd backend
uv run celery -A tasks.celery_app beat --loglevel=info
```

これにより、毎日午前3時（UTC）にSpotifyデータの更新が実行されます。

### 定期更新タスクのカスタマイズ

`tasks/celery_app.py` でスケジュールを変更できます：

```python
# 例: 12時間ごとに実行
celery_app.conf.beat_schedule = {
    "update-spotify-data-daily": {
        "task": "tasks.tasks.update_spotify_data",
        "schedule": crontab(hour="*/12"),
    },
}
```

## 🧪 テスト

### テストの実行

```bash
cd backend
uv run pytest tests/ -v
```

### テストカバレッジ

```bash
# カバレッジを確認する場合
uv run pytest tests/ --cov=. --cov-report=html
```

### テスト対象

- `/analytics/genre-distribution` API
- `/analytics/mood-map` API
- `/analytics/tempo-trends` API
- `/debug/raw-top-tracks` API

## 📝 スクリプト（データ取得）

### 1. 最小スクリプト: ログイン→上位曲取得

```bash
uv run python -m scripts.auth_and_top_tracks
```

初回実行時、ブラウザが自動的に開きSpotifyにログインして権限を許可してください。  
認証後、ターミナルに上位10曲が表示されれば成功です。

### 2. プレイリストとトラックの取得

```bash
uv run python -m scripts.fetch_playlists_and_tracks
```

実行後、`tracks_basic.csv` が作成されます。

### 3. オーディオ特徴量の取得

```bash
uv run python -m scripts.fetch_audio_features
```

`tracks_basic.csv` を読み込んで、各トラックのオーディオ特徴量を取得し、  
`tracks_with_features.csv` に結合して保存します。

## 🏛️ アーキテクチャ

### レイヤー構造

1. **API Layer** (`api/`)
   - FastAPIエンドポイントの定義
   - リクエスト/レスポンスの処理

2. **Service Layer** (`services/`)
   - ビジネスロジックの実装
   - Spotify API連携
   - データ分析処理
   - データベース操作

3. **Model Layer** (`models/`)
   - Pydanticモデルによるデータ検証

4. **Core Layer** (`core/`)
   - データベース設定
   - 設定管理

5. **Task Layer** (`tasks/`)
   - Celeryタスクの定義
   - 定期更新処理

6. **Script Layer** (`scripts/`)
   - スタンドアロンスクリプト
   - CSVエクスポート機能

## 🔒 セキュリティ

- Bearerトークン認証を使用
- CORS設定（本番環境では適切に設定してください）
- 環境変数による機密情報の管理

## 📚 依存関係

主要な依存関係は `pyproject.toml` に記載されています：

- **FastAPI**: Webフレームワーク
- **SQLAlchemy**: ORM
- **Spotipy**: Spotify APIラッパー
- **pandas**: データ分析
- **Celery**: 非同期タスク処理
- **pytest**: テストフレームワーク

## 🐛 トラブルシューティング

### ポート8000が使用中

別のポートを指定：

```bash
uv run uvicorn api.main:app --reload --port 8001
```

### データベースエラー

データベースファイルを削除して再作成：

```bash
rm spotify_analytics.db
uv run python -c "from core.database import init_db; init_db()"
```

### Spotify認証エラー

`.env`ファイルの`SPOTIFY_CLIENT_ID`と`SPOTIFY_CLIENT_SECRET`が正しく設定されているか確認してください。

## 📝 ライセンス

MIT License

