import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, LineController, PointElement, LineElement } from 'chart.js';

Chart.register(CategoryScale, LinearScale, LineController, PointElement, LineElement);


const App = () => {
  const [symbol, setSymbol] = useState('');
  const [chartData, setChartData] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/stock?symbol=${symbol}`);
      const json_data = response.data;
      console.log('Received JSON data:', json_data);
      if (json_data && json_data.results) {
        const chartData = generateChartData(json_data);
        setChartData(chartData);
      }
    } catch (error) {
      console.error('Error fetching stock data:', error);
    }
  };

  const generateChartData = (json_data) => {
    const data = json_data.results.map(result => ({
      t: new Date(result.t),   // Convert timestamp to Date object
      o: result.o,             // Open price
      h: result.h,             // High price
      l: result.l,             // Low price
      c: result.c              // Close price
    }));
  
    return {
      labels: data.map(item => item.t.toLocaleDateString()),  // X-axis labels (dates)
      datasets: [
        {
          label: 'Open',
          data: data.map(item => ({ x: item.t, y: item.o })),  // Format open prices
          borderColor: 'blue',
          fill: false
        },
        {
          label: 'High',
          data: data.map(item => ({ x: item.t, y: item.h })),  // Format high prices
          borderColor: 'green',
          fill: false
        },
        {
          label: 'Low',
          data: data.map(item => ({ x: item.t, y: item.l })),  // Format low prices
          borderColor: 'red',
          fill: false
        },
        {
          label: 'Close',
          data: data.map(item => ({ x: item.t, y: item.c })),  // Format close prices
          borderColor: 'orange',
          fill: false
        }
      ]
    };
  };

  return (
    <div className="App">
      <h1>Stock OHLC Chart</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="symbol">Enter Stock Symbol:</label>
        <input
          type="text"
          id="symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          required
        />
        <button type="submit">Generate Chart</button>
      </form>

      {chartData && (
        <div className="chart-container" style={{ position: 'relative', margin: 'auto', width: '80vw', height: '60vh' }}>
          <Line data={chartData} />
        </div>
      )}
    </div>
  );
};

export default App;
