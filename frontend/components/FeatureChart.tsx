'use client'

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import { AudioFeatures } from '@/lib/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

interface FeatureChartProps {
  features: AudioFeatures[]
}

export default function FeatureChart({ features }: FeatureChartProps) {
  if (features.length === 0) {
    return <div className="text-gray-400 text-center py-8">データがありません</div>
  }

  // 各特徴値を時系列で表示（プレイリストの順序）
  const indices = Array.from({ length: features.length }, (_, i) => i + 1)

  const data = {
    labels: indices.map((i) => `曲 ${i}`),
    datasets: [
      {
        label: 'ダンス性',
        data: features.map((f) => f.danceability),
        borderColor: 'rgba(34, 197, 94, 1)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        fill: false,
        tension: 0.4,
      },
      {
        label: 'エネルギー',
        data: features.map((f) => f.energy),
        borderColor: 'rgba(234, 179, 8, 1)',
        backgroundColor: 'rgba(234, 179, 8, 0.1)',
        fill: false,
        tension: 0.4,
      },
      {
        label: 'ポジティブ度',
        data: features.map((f) => f.valence),
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: false,
        tension: 0.4,
      },
      {
        label: 'テンポ (正規化)',
        data: features.map((f) => f.tempo / 200), // テンポを0-1に正規化
        borderColor: 'rgba(168, 85, 247, 1)',
        backgroundColor: 'rgba(168, 85, 247, 0.1)',
        fill: false,
        tension: 0.4,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    interaction: {
      mode: 'index' as const,
      intersect: false,
    },
    plugins: {
      legend: {
        display: true,
        labels: {
          color: 'rgba(255, 255, 255, 0.9)',
        },
      },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            let label = context.dataset.label || ''
            if (label) {
              label += ': '
            }
            if (context.parsed.y !== null) {
              if (label.includes('テンポ')) {
                label += `${(context.parsed.y * 200).toFixed(1)} BPM`
              } else {
                label += `${(context.parsed.y * 100).toFixed(1)}%`
              }
            }
            return label
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
          maxTicksLimit: 20,
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      y: {
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
          callback: function (value: any) {
            return `${(value * 100).toFixed(0)}%`
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  }

  return (
    <div className="h-96">
      <Line data={data} options={options} />
    </div>
  )
}
