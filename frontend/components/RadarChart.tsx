'use client'

import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'
import { Radar } from 'react-chartjs-2'
import { AudioFeatures } from '@/lib/api'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

interface RadarChartProps {
  features: AudioFeatures[]
}

export default function RadarChart({ features }: RadarChartProps) {
  if (features.length === 0) {
    return <div className="text-gray-400 text-center py-8">データがありません</div>
  }

  // 平均値を計算
  const calculateAverage = (key: keyof AudioFeatures): number => {
    const sum = features.reduce((acc, f) => acc + (f[key] as number), 0)
    return sum / features.length
  }

  const data = {
    labels: [
      'ダンス性',
      'エネルギー',
      'ポジティブ度',
      'アコースティック',
      'インスト',
      'ライブ感',
      'スピーチ性',
    ],
    datasets: [
      {
        label: '平均値',
        data: [
          calculateAverage('danceability'),
          calculateAverage('energy'),
          calculateAverage('valence'),
          calculateAverage('acousticness'),
          calculateAverage('instrumentalness'),
          calculateAverage('liveness'),
          calculateAverage('speechiness'),
        ],
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 2,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      r: {
        beginAtZero: true,
        max: 1,
        ticks: {
          stepSize: 0.2,
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        pointLabels: {
          color: 'rgba(255, 255, 255, 0.9)',
          font: {
            size: 12,
          },
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
          backdropColor: 'transparent',
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            return `${context.label}: ${(context.parsed.r * 100).toFixed(1)}%`
          },
        },
      },
    },
  }

  return (
    <div className="h-64">
      <Radar data={data} options={options} />
    </div>
  )
}
