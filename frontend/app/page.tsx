'use client'

import { useState } from 'react'
import SpotifyAuth from '@/components/SpotifyAuth'
import PlaylistSelector from '@/components/PlaylistSelector'
import PlaylistAnalysis from '@/components/PlaylistAnalysis'

export default function Home() {
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [selectedPlaylistId, setSelectedPlaylistId] = useState<string | null>(null)

  return (
    <main className="min-h-screen bg-gradient-to-br from-green-900 via-black to-purple-900 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-2 text-center">
          🎵 Spotify プレイリスト分析ツール
        </h1>
        <p className="text-center text-gray-300 mb-8">
          あなたの音楽の好みを可視化して、新しい音楽を発見しましょう
        </p>

        {!accessToken ? (
          <SpotifyAuth onAuthSuccess={setAccessToken} />
        ) : !selectedPlaylistId ? (
          <PlaylistSelector
            accessToken={accessToken}
            onSelectPlaylist={setSelectedPlaylistId}
          />
        ) : (
          <PlaylistAnalysis
            accessToken={accessToken}
            playlistId={selectedPlaylistId}
            onBack={() => setSelectedPlaylistId(null)}
          />
        )}
      </div>
    </main>
  )
}
