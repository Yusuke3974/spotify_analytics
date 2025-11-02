'use client'

import { useEffect } from 'react'

interface SpotifyAuthProps {
  onAuthSuccess: (token: string) => void
}

export default function SpotifyAuth({ onAuthSuccess }: SpotifyAuthProps) {
  useEffect(() => {
    // URLフラグメントからアクセストークンを取得
    const hash = window.location.hash
    if (hash) {
      const params = new URLSearchParams(hash.substring(1))
      const accessToken = params.get('access_token')
      if (accessToken) {
        onAuthSuccess(accessToken)
        // URLをクリーンアップ
        window.history.replaceState(null, '', window.location.pathname)
      }
    }
  }, [onAuthSuccess])

  const handleLogin = () => {
    const clientId = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID || ''
    const redirectUri =
      process.env.NEXT_PUBLIC_SPOTIFY_REDIRECT_URI || window.location.origin
    const scopes = [
      'user-read-private',
      'user-read-email',
      'user-library-read',
      'playlist-read-private',
      'playlist-read-collaborative',
    ].join('%20')

    const authUrl = `https://accounts.spotify.com/authorize?client_id=${clientId}&response_type=token&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${scopes}`

    window.location.href = authUrl
  }

  return (
    <div className="flex justify-center items-center min-h-[400px]">
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-8 text-center">
        <h2 className="text-2xl font-bold text-white mb-4">
          Spotifyに接続
        </h2>
        <p className="text-gray-300 mb-6">
          プレイリストを分析するために、Spotifyアカウントに接続してください
        </p>
        <button
          onClick={handleLogin}
          className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-full transition-colors"
        >
          Spotifyでログイン
        </button>
        <p className="text-xs text-gray-400 mt-4">
          * Spotify Developer Appの設定が必要です
        </p>
      </div>
    </div>
  )
}
