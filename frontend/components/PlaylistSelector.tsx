'use client'

import { useState, useEffect } from 'react'
import { getPlaylists, Playlist } from '@/lib/api'

interface PlaylistSelectorProps {
  accessToken: string
  onSelectPlaylist: (playlistId: string) => void
}

export default function PlaylistSelector({
  accessToken,
  onSelectPlaylist,
}: PlaylistSelectorProps) {
  const [playlists, setPlaylists] = useState<Playlist[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchPlaylists() {
      try {
        setLoading(true)
        const data = await getPlaylists(accessToken)
        setPlaylists(data)
      } catch (err) {
        setError('プレイリストの取得に失敗しました')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchPlaylists()
  }, [accessToken])

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-white text-xl">読み込み中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="bg-red-500/20 backdrop-blur-lg rounded-lg p-8 text-center">
          <p className="text-red-300">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-white mb-6">
        プレイリストを選択
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {playlists.map((playlist) => (
          <div
            key={playlist.id}
            onClick={() => onSelectPlaylist(playlist.id)}
            className="bg-white/10 backdrop-blur-lg rounded-lg p-4 cursor-pointer hover:bg-white/20 transition-all"
          >
            <div className="aspect-square mb-3 bg-gray-700 rounded overflow-hidden">
              {playlist.image_url ? (
                <img
                  src={playlist.image_url}
                  alt={playlist.name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  🎵
                </div>
              )}
            </div>
            <h3 className="text-white font-semibold truncate">
              {playlist.name}
            </h3>
            <p className="text-gray-400 text-sm mt-1">
              {playlist.track_count}曲
            </p>
          </div>
        ))}
      </div>
      {playlists.length === 0 && (
        <div className="text-center text-gray-400 mt-8">
          プレイリストが見つかりませんでした
        </div>
      )}
    </div>
  )
}
