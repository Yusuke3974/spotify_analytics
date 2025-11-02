'use client'

import { useState, useEffect } from 'react'
import HistoryList from '@/components/HistoryList'
import TempoChart from '@/components/TempoChart'
import MoodScatter from '@/components/MoodScatter'
import { getHistory, type AnalysisHistory } from '@/lib/api'

export default function DashboardPage() {
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [history, setHistory] = useState<AnalysisHistory[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedHistory, setSelectedHistory] = useState<AnalysisHistory | null>(null)

  useEffect(() => {
    // ローカルストレージからアクセストークンを取得
    const token = localStorage.getItem('spotify_access_token')
    if (token) {
      setAccessToken(token)
      fetchHistory(token)
    } else {
      setError('アクセストークンが見つかりません。先にSpotifyでログインしてください。')
      setLoading(false)
    }
  }, [])

  const fetchHistory = async (token: string) => {
    try {
      setLoading(true)
      const data = await getHistory(token)
      setHistory(data)
      // 最新の履歴を選択
      if (data.length > 0) {
        setSelectedHistory(data[0])
      }
      setError(null)
    } catch (err) {
      setError('履歴の取得に失敗しました。')
      console.error('Error fetching history:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleHistorySelect = (item: AnalysisHistory) => {
    setSelectedHistory(item)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">読み込み中...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">分析履歴ダッシュボード</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 履歴リスト（左側） */}
          <div className="lg:col-span-1">
            <HistoryList
              history={history}
              selectedId={selectedHistory?.id}
              onSelect={handleHistorySelect}
            />
          </div>

          {/* 可視化エリア（右側） */}
          <div className="lg:col-span-2 space-y-6">
            {selectedHistory ? (
              <>
                {/* テンポ分布チャート */}
                {selectedHistory.analysis_type === 'tempo' && selectedHistory.result.mean_tempo !== undefined && (
                  <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">テンポ分布</h2>
                    <TempoChart data={{
                      mean_tempo: selectedHistory.result.mean_tempo,
                      std_tempo: selectedHistory.result.std_tempo,
                      distribution: selectedHistory.result.distribution as Array<{ range: string; count: number }> | undefined,
                    }} />
                  </div>
                )}

                {/* ムードマップ */}
                {selectedHistory.analysis_type === 'mood' && selectedHistory.result.mood_map && (
                  <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">ムードマップ (Valence × Energy)</h2>
                    <MoodScatter data={selectedHistory.result.mood_map} />
                  </div>
                )}

                {/* ジャンル分布 */}
                {selectedHistory.analysis_type === 'genre' && selectedHistory.result.distribution && (
                  <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">ジャンル分布</h2>
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                      {(selectedHistory.result.distribution as Array<{ genre: string; count: number }>).map((item, index: number) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                          <span className="font-medium">{item.genre}</span>
                          <span className="text-blue-600 font-semibold">{item.count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* 選択された履歴の情報 */}
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <h2 className="text-xl font-semibold mb-4">分析情報</h2>
                  <div className="space-y-2 text-sm">
                    <p><span className="font-medium">分析タイプ:</span> {selectedHistory.analysis_type}</p>
                    <p><span className="font-medium">期間:</span> {selectedHistory.time_range}</p>
                    <p><span className="font-medium">作成日時:</span> {new Date(selectedHistory.created_at).toLocaleString('ja-JP')}</p>
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-white p-6 rounded-lg shadow-md">
                <p className="text-gray-500">履歴を選択してください</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

