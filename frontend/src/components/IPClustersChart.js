import React from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const AnomaliesChart = ({ data }) => {
  // Initialize risk counts and IP storage arrays for 3 categories
  const riskCounts = { 'low risk': 0, 'medium risk': 0, 'high risk': 0 };
  const ipAddresses = { 'low risk': [], 'medium risk': [], 'high risk': [] };

  data.forEach(item => {
    const ip = item[1];
    const riskCategory = item[6].toLowerCase();

    if (riskCounts[riskCategory] !== undefined) {
        riskCounts[riskCategory]++;
        ipAddresses[riskCategory].push(ip); // Store IPs by category
    } else {
        console.log('Unrecognized risk category:', riskCategory);
    }
  });

  const chartData = {
    labels: ['Low Risk', 'Medium Risk', 'High Risk'],
    datasets: [
      {
        data: [riskCounts['low risk'], riskCounts['medium risk'], riskCounts['high risk']],
        backgroundColor: ['#3eff00', '#f7ff00', '#ff0000'], // Green, Yellow, Red
        hoverOffset: 4,
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
            const category = tooltipItem.label.toLowerCase();
            const ipsInCategory = ipAddresses[category];
            return `${tooltipItem.label}: ${tooltipItem.raw} IPs (${ipsInCategory.join(', ')})`;
          },
        },
      },
    },
  };

  return (
    <div>
      <h3>Anomalies Visualization</h3>
      <Pie data={chartData} options={options} />
    </div>
  );
};

export default AnomaliesChart;