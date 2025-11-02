'use client'

import { useEffect, useRef } from 'react'
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
import { Scatter } from 'react-chartjs-2'

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

interface MoodScatterProps {
  data: Array<{ track: string; valence: number; energy: number }>
}

export default function MoodScatter({ data }: MoodScatterProps) {
  const chartRef = useRef<ChartJS<'scatter'>>(null)

  if (!data || data.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        データがありません
      </div>
    )
  }

  // データポイントを準備
  const scatterData = data.map((item) => ({
    x: item.valence,
    y: item.energy,
    label: item.track,
  }))

  const chartData = {
    datasets: [
      {
        label: 'トラック',
        data: scatterData,
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgba(59, 130, 246, 1)',
        pointRadius: 6,
        pointHoverRadius: 8,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Valence（ポジティブさ） × Energy（エネルギー）',
        font: {
          size: 14,
        },
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const point = context.raw
            return [
              `トラック: ${point.label || '不明'}`,
              `Valence: ${point.x.toFixed(2)}`,
              `Energy: ${point.y.toFixed(2)}`,
            ]
          },
        },
      },
    },
    scales: {
      x: {
        type: 'linear' as const,
        position: 'bottom' as const,
        title: {
          display: true,
          text: 'Valence（ポジティブさ）',
        },
        min: 0,
        max: 1,
      },
      y: {
        type: 'linear' as const,
        title: {
          display: true,
          text: 'Energy（エネルギー）',
        },
        min: 0,
        max: 1,
      },
    },
  }

  return (
    <div className="h-96">
      <Scatter ref={chartRef} data={chartData} options={options} />
    </div>
  )
}

