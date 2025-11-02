'use client'

import { useState, useEffect } from 'react'
import { analyzePlaylist, AudioFeatures, Track, PlaylistStats } from '@/lib/api'
import FeatureChart from './FeatureChart'
import FeatureHistogram from './FeatureHistogram'
import RadarChart from './RadarChart'

interface PlaylistAnalysisProps {
  accessToken: string
  playlistId: string
  onBack: () => void
}

export default function PlaylistAnalysis({
  accessToken,
  playlistId,
  onBack,
}: PlaylistAnalysisProps) {
  const [playlistName, setPlaylistName] = useState<string>('')
  const [tracks, setTracks] = useState<Track[]>([])
  const [features, setFeatures] = useState<AudioFeatures[]>([])
  const [stats, setStats] = useState<PlaylistStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true)
        
        // プレイリスト全体を分析
        const analysis = await analyzePlaylist(accessToken, playlistId)
        setPlaylistName(analysis.playlist.name)
        setTracks(analysis.tracks)
        setFeatures(analysis.features)
        setStats(analysis.stats)
      } catch (err) {
        setError('データの取得に失敗しました')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [accessToken, playlistId])

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-white text-xl">分析中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="bg-red-500/20 backdrop-blur-lg rounded-lg p-8 text-center">
          <p className="text-red-300">{error}</p>
          <button
            onClick={onBack}
            className="mt-4 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            戻る
          </button>
        </div>
      </div>
    )
  }

  // 統計情報から平均値を取得
  const averages = stats
    ? {
        danceability: stats.averages.danceability || 0,
        energy: stats.averages.energy || 0,
        valence: stats.averages.valence || 0,
        tempo: stats.averages.tempo || 0,
        acousticness: stats.averages.acousticness || 0,
        instrumentalness: stats.averages.instrumentalness || 0,
        liveness: stats.averages.liveness || 0,
        speechiness: stats.averages.speechiness || 0,
      }
    : {
        danceability: 0,
        energy: 0,
        valence: 0,
        tempo: 0,
        acousticness: 0,
        instrumentalness: 0,
        liveness: 0,
        speechiness: 0,
      }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex items-center mb-6">
        <button
          onClick={onBack}
          className="mr-4 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
        >
          ← 戻る
        </button>
        <h2 className="text-3xl font-bold text-white">{playlistName}</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4">基本統計</h3>
          <div className="space-y-2">
            <div className="flex justify-between text-gray-300">
              <span>総曲数:</span>
              <span className="text-white font-semibold">
                {stats ? stats.total_tracks : tracks.length}曲
              </span>
            </div>
            <div className="flex justify-between text-gray-300">
              <span>分析可能曲数:</span>
              <span className="text-white font-semibold">
                {stats ? stats.analyzed_tracks : features.length}曲
              </span>
            </div>
            <div className="flex justify-between text-gray-300">
              <span>平均テンポ:</span>
              <span className="text-white font-semibold">
                {averages.tempo > 0 ? `${averages.tempo.toFixed(1)} BPM` : '-'}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4">平均特徴値</h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">ダンス性:</span>
              <div className="flex-1 mx-4 bg-gray-700 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${averages.danceability * 100}%` }}
                />
              </div>
              <span className="text-white font-semibold w-12 text-right">
                {(averages.danceability * 100).toFixed(0)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">エネルギー:</span>
              <div className="flex-1 mx-4 bg-gray-700 rounded-full h-2">
                <div
                  className="bg-yellow-500 h-2 rounded-full"
                  style={{ width: `${averages.energy * 100}%` }}
                />
              </div>
              <span className="text-white font-semibold w-12 text-right">
                {(averages.energy * 100).toFixed(0)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">ポジティブ度:</span>
              <div className="flex-1 mx-4 bg-gray-700 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full"
                  style={{ width: `${averages.valence * 100}%` }}
                />
              </div>
              <span className="text-white font-semibold w-12 text-right">
                {(averages.valence * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4">レーダーチャート</h3>
          <RadarChart features={features} />
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h3 className="text-xl font-bold text-white mb-4">特徴値の分布</h3>
          <FeatureHistogram features={features} />
        </div>
      </div>

      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-4">詳細分析</h3>
        <FeatureChart features={features} />
      </div>
    </div>
  )
}
