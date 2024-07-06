// Function to load JSON data
async function loadJSON(filePath) {
  try {
      const response = await fetch(filePath);
      if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
      }
      return await response.json();
  } catch (error) {
      console.error('Error loading JSON data:', error);
  }
}

// Load data for line and bar charts
loadJSON('line_bar_data.json').then(lineBarData => {
  if (lineBarData) {
      const lineChart = echarts.init(document.getElementById('lineChart'));
      const barChart = echarts.init(document.getElementById('barChart'));

      const lineChartOptions = {
          title: { text: 'Monthly Sales Data' },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: lineBarData.months },
          yAxis: { type: 'value' },
          series: [{ data: lineBarData.sales, type: 'line', smooth: true }]
      };

      const barChartOptions = {
          title: { text: 'Monthly Sales Data' },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: lineBarData.months },
          yAxis: { type: 'value' },
          series: [{ data: lineBarData.sales, type: 'bar' }]
      };

      lineChart.setOption(lineChartOptions);
      barChart.setOption(barChartOptions);
  }
});

// Load data for pie chart
loadJSON('pie_data.json').then(pieData => {
  if (pieData) {
      const pieChart = echarts.init(document.getElementById('pieChart'));

      const pieChartOptions = {
          title: { text: 'Product Sales Share', x: 'center' },
          tooltip: { trigger: 'item' },
          series: [{
              type: 'pie',
              radius: '50%',
              data: pieData,
              emphasis: {
                  itemStyle: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
              }
          }]
      };
      pieChart.setOption(pieChartOptions);
  }
});

// Ensure charts resize responsively
window.addEventListener('resize', function () {
  const lineChart = echarts.getInstanceByDom(document.getElementById('lineChart'));
  const barChart = echarts.getInstanceByDom(document.getElementById('barChart'));
  const pieChart = echarts.getInstanceByDom(document.getElementById('pieChart'));

  if (lineChart) lineChart.resize();
  if (barChart) barChart.resize();
  if (pieChart) pieChart.resize();
});
