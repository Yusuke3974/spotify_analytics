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
# Spotify API設定
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:3000

# API設定（Next.js用）
NEXT_PUBLIC_SPOTIFY_CLIENT_ID=your_spotify_client_id_here
NEXT_PUBLIC_SPOTIFY_REDIRECT_URI=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

`.env.example`を参考にしてください。

## 📊 動作確認方法

### バックエンド（FastAPI）の起動

ターミナル1で以下を実行：

```bash
# uvで仮想環境を有効化してから実行
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\Activate.ps1  # Windows PowerShell

# バックエンド起動
uvicorn backend.main:app --reload --port 8000
```

または、uvを使用して直接実行：

```bash
uv run uvicorn backend.main:app --reload --port 8000
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
├── backend/                 # FastAPIバックエンド
│   ├── __init__.py
│   ├── main.py             # FastAPIアプリケーション
│   ├── models.py           # Pydanticモデル
│   └── spotify_service.py  # Spotify API連携サービス
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
├── pyproject.toml           # Python依存関係（uv使用）
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

## 📝 ライセンス

MIT License
