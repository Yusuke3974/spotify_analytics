# 🎵 Spotify プレイリスト分析ツール

Spotifyプレイリストを分析して、あなたの音楽の好みを可視化するツールです。

## ✨ 機能

### Step 1: プレイリスト基本分析 ✅
- 曲ごとの特徴値分析（danceability, energy, tempo, valenceなど）
- ヒストグラム表示
- 平均値表示
- レーダーチャート表示

### Step 2: ユーザー嗜好分析（今後実装予定）
- k-meansクラスタリングで「あなたの曲傾向タイプ」を分類
- 各クラスタの代表曲を自動抽出

### Step 3: おすすめ曲レコメンド（今後実装予定）
- 類似特徴を持つ未聴曲をSpotify APIから提案
- 「あなたに合う未発掘アーティスト」など

### Step 4: 時系列分析（今後実装予定）
- 朝・夜の聴取傾向
- 「感情マップ」表示（Valence×Energy）

## 🛠️ 技術スタック

- **バックエンド**: Python + FastAPI
- **データ分析**: pandas, numpy, scikit-learn
- **Spotify API**: spotipy（OAuth2対応のPythonラッパ）
- **パッケージ管理**: uv（Python）
- **可視化**: Chart.js（フロントエンド）
- **フロントエンド**: Next.js 14 + React + TypeScript + Tailwind CSS
- **デプロイ**: Streamlit Cloud / Render / Vercel
- **DB（任意）**: SQLite（履歴保存）

## 🚀 セットアップ

### 前提条件

- Python 3.10以上
- Node.js 18以上
- [uv](https://github.com/astral-sh/uv) (Pythonパッケージ管理ツール)

### 1. uvのインストール

#### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

詳細は [uv公式ドキュメント](https://github.com/astral-sh/uv) を参照してください。

### 2. リポジトリのクローンとディレクトリ移動

```bash
git clone <repository-url>
cd spotify_analytics
```

### 3. Python依存関係のインストール（uv使用）

```bash
uv sync
```

これにより、仮想環境が自動的に作成され、依存関係がインストールされます。

### 4. Node.js依存関係のインストール

```bash
npm install
```

### 5. Spotify Developer Appの設定

1. [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)にアクセス
2. 新しいアプリを作成
3. リダイレクトURIを設定: `http://localhost:3000`

### 6. 環境変数の設定

`.env`ファイルを作成し、以下の環境変数を設定してください：

```env
# Spotify API設定（スクリプト用）
SPOTIPY_CLIENT_ID=your_spotify_client_id_here
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8080/callback

# FastAPI用設定
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:3000

# Next.js用環境変数（NEXT_PUBLIC_プレフィックスが必要）
NEXT_PUBLIC_SPOTIFY_CLIENT_ID=your_spotify_client_id_here
NEXT_PUBLIC_SPOTIFY_REDIRECT_URI=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

`.env.example`を参考にしてください。

**重要**: Spotify Developer Dashboardで以下のリダイレクトURIを追加してください：
- `http://localhost:8080/callback`（スクリプト用）
- `http://localhost:3000`（Next.jsアプリ用）

## 📊 動作確認方法

### バックエンド（FastAPI）の起動

ターミナル1で以下を実行（プロジェクトルートから）：

```bash
# uvで仮想環境を有効化してから実行
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\Activate.ps1  # Windows PowerShell

# バックエンド起動（プロジェクトルートから実行）
cd backend
uvicorn api.main:app --reload --port 8000
```

または、プロジェクトルートから直接実行：

```bash
# プロジェクトルートから
uv run uvicorn backend.api.main:app --reload --port 8000
```

バックエンドAPIが起動したら、以下で確認できます：
- APIドキュメント: http://localhost:8000/docs
- ヘルスチェック: http://localhost:8000/

### フロントエンド（Next.js）の起動

ターミナル2で以下を実行：

```bash
cd frontend
npm install
npm run dev
```

ブラウザで http://localhost:3000 が自動的に開きます。

### 動作確認の手順

1. **Spotifyに接続**
   - 「Spotifyでログイン」ボタンをクリック
   - Spotifyの認証画面でログインして権限を許可
   - リダイレクト後、アクセストークンが自動的に取得されます

2. **プレイリストを選択**
   - プレイリスト一覧から分析したいプレイリストを選択

3. **結果を確認**
   - 統計情報（総曲数、平均テンポなど）
   - 平均特徴値（ダンス性、エネルギー、ポジティブ度など）
   - レーダーチャート
   - ヒストグラム
   - 詳細分析チャート

### トラブルシューティング

#### uvがインストールされていない
- [uv公式ドキュメント](https://github.com/astral-sh/uv) を参照してインストールしてください

#### バックエンドが起動しない
- ポート8000が使用中の場合、別のポートを指定: `--port 8001`
- `.env`ファイルの設定を確認してください

#### フロントエンドが起動しない
- Node.jsがインストールされているか確認: `node --version`
- `frontend`ディレクトリで`npm install`が完了しているか確認
- `.env`ファイルの`NEXT_PUBLIC_*`変数が設定されているか確認

#### Spotify認証エラー
- `.env`ファイルの`SPOTIFY_CLIENT_ID`と`SPOTIFY_CLIENT_SECRET`が正しく設定されているか確認
- リダイレクトURIがSpotify Developer Dashboardで設定されているか確認

#### API接続エラー
- バックエンドが起動しているか確認
- `.env`の`NEXT_PUBLIC_API_BASE_URL`が正しいか確認（デフォルト: `http://localhost:8000`）

## 📁 プロジェクト構造

```
spotify_analytics/
├── backend/                 # FastAPIバックエンド + データ取得スクリプト
│   ├── api/                  # FastAPIアプリケーション
│   │   ├── __init__.py
│   │   └── main.py           # FastAPIエントリポイント
│   ├── core/                  # コア設定
│   │   ├── __init__.py
│   │   └── database.py        # SQLAlchemy設定とDBモデル
│   ├── services/              # ビジネスロジック層
│   │   ├── __init__.py
│   │   ├── spotify_client.py  # SpotipyでSpotify API呼び出し
│   │   ├── data_analyzer.py   # pandasで分析処理
│   │   └── db_service.py      # データベース操作サービス
│   ├── models/                # データモデル
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydanticモデル（APIレスポンス定義）
│   ├── tasks/                 # Celeryタスク
│   │   ├── __init__.py
│   │   ├── celery_app.py     # Celery設定
│   │   └── tasks.py           # Celeryタスク（定期更新）
│   ├── scripts/               # データ取得スクリプト
│   │   ├── __init__.py
│   │   ├── auth_and_top_tracks.py      # 最小スクリプト（ログイン→上位曲）
│   │   ├── fetch_playlists_and_tracks.py # プレイリストとトラック取得
│   │   └── fetch_audio_features.py      # オーディオ特徴量取得
│   ├── tests/                 # テストコード
│   │   ├── __init__.py
│   │   └── test_analytics.py  # pytest + HTTPXテスト
│   ├── pyproject.toml         # Python依存関係（uv使用）
│   ├── pytest.ini             # pytest設定
│   └── README.md               # バックエンドREADME
├── frontend/                # Next.js フロントエンド
│   ├── app/                 # Next.js アプリケーション（App Router）
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/          # Reactコンポーネント
│   │   ├── SpotifyAuth.tsx
│   │   ├── PlaylistSelector.tsx
│   │   ├── PlaylistAnalysis.tsx
│   │   ├── RadarChart.tsx
│   │   ├── FeatureChart.tsx
│   │   └── FeatureHistogram.tsx
│   ├── lib/                 # ユーティリティ
│   │   └── api.ts           # FastAPIバックエンドとの通信クライアント
│   ├── next.config.js       # Next.js設定
│   ├── package.json         # Node.js依存関係
│   ├── tsconfig.json        # TypeScript設定
│   ├── tailwind.config.ts   # Tailwind CSS設定
│   └── postcss.config.js    # PostCSS設定
├── pyproject.toml           # Python依存関係（uv使用）- プロジェクトルート（オプション）
├── .env.example             # 環境変数テンプレート
├── .gitignore
└── README.md
```

## 🔧 開発

### Pythonコードフォーマット（オプション）

```bash
uv add --dev black isort
uv run black .
uv run isort .
```

### 型チェック（オプション）

```bash
uv add --dev mypy
uv run mypy backend/
```

### Next.js開発

```bash
cd frontend

# 開発サーバー
npm run dev

# ビルド
npm run build

# 本番サーバー起動
npm start
```

## 📊 データ取得スクリプト（CSVエクスポート）

Spotifyからデータを取得してCSVファイルに保存するスクリプトを用意しています。

### 事前準備

Spotify Developer Dashboardで以下のリダイレクトURIを追加してください：
- `http://localhost:8080/callback`

`.env`ファイルに以下を設定してください：
```env
SPOTIPY_CLIENT_ID=your_spotify_client_id_here
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8080/callback
```

### 1. 最小スクリプト: ログイン→上位曲取得

```bash
uv run python -m backend.scripts.auth_and_top_tracks
```

初回実行時、ブラウザが自動的に開きSpotifyにログインして権限を許可してください。  
認証後、ターミナルに上位10曲が表示されれば成功です。

以降は `.cache-spotify` のリフレッシュトークンで自動再認証されます。

### 2. プレイリストとトラックの取得

```bash
uv run python -m backend.scripts.fetch_playlists_and_tracks
```

実行後、`tracks_basic.csv` が作成されます。
- すべてのプレイリスト
- 各プレイリスト内のトラック情報（名前、アーティスト、アルバムなど）

### 3. オーディオ特徴量の取得

```bash
uv run python -m backend.scripts.fetch_audio_features
```

`tracks_basic.csv` を読み込んで、各トラックのオーディオ特徴量（danceability, energy, tempoなど）を取得し、  
`tracks_with_features.csv` に結合して保存します。

### 生成されるCSVファイル

- `tracks_basic.csv`: トラックの基本情報（プレイリスト、アーティスト、アルバムなど）
- `tracks_with_features.csv`: 基本情報 + オーディオ特徴量（danceability, energy, valence, tempoなど）

これらのCSVファイルをpandasで読み込んで分析に使用できます。

### スコープの拡張

デフォルトでは最小限のスコープを使用していますが、より多くのデータを取得したい場合は、スクリプト内の `SCOPE` 変数を変更してください：

```python
SCOPE = "user-top-read playlist-read-private playlist-read-collaborative user-read-recently-played user-library-read"
```

## 🧪 APIテスト（cURL例）

バックエンドが起動したら、以下のコマンドでAPIをテストできます：

### ジャンル分布
```bash
curl -X GET "http://localhost:8000/analytics/genre-distribution?limit=50&time_range=medium_term" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### ムードマップ（valence × energy）
```bash
curl -X GET "http://localhost:8000/analytics/mood-map?limit=50&time_range=medium_term" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### テンポトレンド
```bash
curl -X GET "http://localhost:8000/analytics/tempo-trends?limit=50&time_range=medium_term" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

### デバッグ: 生データの確認
```bash
curl -X GET "http://localhost:8000/debug/raw-top-tracks?limit=20&time_range=medium_term" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" | jq .
```

**注意**: `YOUR_ACCESS_TOKEN` は実際のSpotifyアクセストークンに置き換えてください。

### Swagger UIでテスト

1. バックエンドを起動: `cd backend && uv run uvicorn api.main:app --reload`
2. ブラウザで http://localhost:8000/docs を開く
3. 「Authorize」ボタンをクリックして、Bearerトークンを入力: `YOUR_ACCESS_TOKEN`
4. 各エンドポイントをクリックして「Try it out」→「Execute」でテスト

## 🗄️ データベースと定期更新

### データベース設定

SQLiteデータベースは自動的に作成されます（`spotify_analytics.db`）。

```bash
# データベースを初期化（初回起動時に自動実行）
# backend/main.py が起動時に自動実行します
```

### Celery + Redis の起動

#### 1. Redisの起動

```bash
# Dockerを使用する場合
docker run -d -p 6379:6379 redis:latest

# または、ローカルにRedisがインストールされている場合
redis-server
```

#### 2. Celery Workerの起動

```bash
cd backend
celery -A celery_app worker --loglevel=info
```

#### 3. Celery Beat（スケジューラー）の起動

```bash
cd backend
celery -A celery_app beat --loglevel=info
```

これにより、毎日午前3時（UTC）にSpotifyデータの更新が実行されます。

### 定期更新タスクのカスタマイズ

`backend/celery_app.py` でスケジュールを変更できます：

```python
# 例: 12時間ごとに実行
celery_app.conf.beat_schedule = {
    "update-spotify-data-daily": {
        "task": "backend.tasks.update_spotify_data",
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

### 動作確認の流れ

1. **依存関係のインストール**
   ```bash
   cd backend
   uv sync
   ```

2. **データベースの初期化**（自動実行されます）
   ```bash
   cd backend
   uv run python -c "from core.database import init_db; init_db()"
   ```

3. **バックエンドの起動**
```bash
cd backend
uv run uvicorn api.main:app --reload
   ```

4. **Swagger UIで確認**
   - http://localhost:8000/docs を開く
   - 「Authorize」でBearerトークンを設定
   - 各エンドポイントをテスト

5. **テストの実行**
   ```bash
   cd backend
   uv run pytest tests/ -v
   ```

6. **Celery + Redisの起動**（オプション）
   ```bash
   # Redis起動（別ターミナル）
   docker run -d -p 6379:6379 redis:latest
   
   # Celery Worker起動（別ターミナル）
   cd backend
   celery -A celery_app worker --loglevel=info
   
   # Celery Beat起動（別ターミナル）
   cd backend
   celery -A celery_app beat --loglevel=info
   ```

## 📝 ライセンス

MIT License
