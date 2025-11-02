'use client'

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar } from 'react-chartjs-2'
import { AudioFeatures } from '@/lib/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface FeatureHistogramProps {
  features: AudioFeatures[]
}

export default function FeatureHistogram({ features }: FeatureHistogramProps) {
  if (features.length === 0) {
    return <div className="text-gray-400 text-center py-8">データがありません</div>
  }

  // ヒストグラム用のビンを作成
  const createBins = (values: number[], bins: number = 10) => {
    const min = Math.min(...values)
    const max = Math.max(...values)
    const binSize = (max - min) / bins
    const binCounts = new Array(bins).fill(0)
    
    values.forEach((value) => {
      const binIndex = Math.min(Math.floor((value - min) / binSize), bins - 1)
      binCounts[binIndex]++
    })

    return {
      labels: Array.from({ length: bins }, (_, i) => {
        const start = min + binSize * i
        const end = min + binSize * (i + 1)
        return `${start.toFixed(2)}-${end.toFixed(2)}`
      }),
      data: binCounts,
    }
  }

  const danceabilityValues = features.map((f) => f.danceability)
  const energyValues = features.map((f) => f.energy)
  const valenceValues = features.map((f) => f.valence)

  const danceabilityBins = createBins(danceabilityValues, 8)
  const energyBins = createBins(energyValues, 8)
  const valenceBins = createBins(valenceValues, 8)

  const data = {
    labels: danceabilityBins.labels,
    datasets: [
      {
        label: 'ダンス性',
        data: danceabilityBins.data,
        backgroundColor: 'rgba(34, 197, 94, 0.5)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 1,
      },
      {
        label: 'エネルギー',
        data: energyBins.data,
        backgroundColor: 'rgba(234, 179, 8, 0.5)',
        borderColor: 'rgba(234, 179, 8, 1)',
        borderWidth: 1,
      },
      {
        label: 'ポジティブ度',
        data: valenceBins.data,
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: true,
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
            return `${context.dataset.label}: ${context.parsed.y}曲`
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
          maxRotation: 45,
          minRotation: 45,
          font: {
            size: 10,
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      y: {
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
          stepSize: 1,
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  }

  return (
    <div className="h-64">
      <Bar data={data} options={options} />
    </div>
  )
}
