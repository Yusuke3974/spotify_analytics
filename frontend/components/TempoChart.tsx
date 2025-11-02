'use client'

import { useEffect, useRef } from 'react'
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

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface TempoChartProps {
  data: {
    mean_tempo?: number
    std_tempo?: number
    distribution?: Array<{ range: string; count: number }>
  }
}

export default function TempoChart({ data }: TempoChartProps) {
  const chartRef = useRef<ChartJS<'bar'>>(null)

  if (!data.distribution || data.distribution.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        データがありません
      </div>
    )
  }

  const chartData = {
    labels: data.distribution.map((item) => item.range),
    datasets: [
      {
        label: 'トラック数',
        data: data.distribution.map((item) => item.count),
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
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
        text: data.mean_tempo !== undefined
          ? `平均テンポ: ${data.mean_tempo.toFixed(1)} BPM (標準偏差: ${data.std_tempo?.toFixed(1) || 0})`
          : 'テンポ分布',
        font: {
          size: 14,
        },
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            return `${context.parsed.y} トラック`
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  }

  return (
    <div className="h-64">
      <Bar ref={chartRef} data={chartData} options={options} />
    </div>
  )
}

