'use client'

import { AnalysisHistory } from '@/lib/api'

interface HistoryListProps {
  history: AnalysisHistory[]
  selectedId?: number
  onSelect: (item: AnalysisHistory) => void
}

export default function HistoryList({ history, selectedId, onSelect }: HistoryListProps) {
  const getAnalysisTypeLabel = (type: string) => {
    switch (type) {
      case 'genre':
        return 'ジャンル分布'
      case 'mood':
        return 'ムードマップ'
      case 'tempo':
        return 'テンポ分析'
      default:
        return type
    }
  }

  const getTimeRangeLabel = (range: string) => {
    switch (range) {
      case 'short_term':
        return '短期（4週間）'
      case 'medium_term':
        return '中期（6ヶ月）'
      case 'long_term':
        return '長期（全期間）'
      default:
        return range
    }
  }

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString)
      return date.toLocaleString('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      })
    } catch {
      return dateString
    }
  }

  if (history.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">履歴</h2>
        <p className="text-gray-500 text-sm">分析履歴がありません</p>
      </div>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">履歴</h2>
      <div className="space-y-2 max-h-[600px] overflow-y-auto">
        {history.map((item) => (
          <button
            key={item.id}
            onClick={() => onSelect(item)}
            className={`w-full text-left p-4 rounded-lg border-2 transition-colors ${
              selectedId === item.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-sm text-gray-900">
                {getAnalysisTypeLabel(item.analysis_type)}
              </span>
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                {getTimeRangeLabel(item.time_range)}
              </span>
            </div>
            <p className="text-xs text-gray-500">{formatDate(item.created_at)}</p>
          </button>
        ))}
      </div>
    </div>
  )
}

