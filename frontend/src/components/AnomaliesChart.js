import React from 'react';
import { Line } from 'react-chartjs-2';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  LineElement, 
  PointElement, 
  Title, 
  Tooltip, 
  Legend 
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

const AnomaliesChart = ({ data }) => {

  const labels = data.map(item => item[1]); // IP addresses
  const inBytes = data.map(item => item[2]); // In bytes
  const outBytes = data.map(item => item[3]); // Out bytes

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: 'In Bytes',
        data: inBytes,
        borderColor: 'rgba(255, 50, 50, 1)',
        backgroundColor: 'rgba(255, 50, 50, 0.2)',
        borderWidth: 1,
      },
      {
        label: 'Out Bytes',
        data: outBytes,
        borderColor: 'rgba(153, 102, 255, 1)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            return `${tooltipItem.dataset.label}: ${tooltipItem.raw}`;
          },
        },
      },
    },
  };

  return (
    <div>
      <h3>Anomalies Visualization</h3>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default AnomaliesChart;