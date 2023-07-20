/* global Chart, coreui */

/**
 * --------------------------------------------------------------------------
 * CoreUI Boostrap Admin Template (v4.2.2): main.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

// Disable the on-canvas tooltip
Chart.defaults.pointHitDetectionRadius = 1;
Chart.defaults.plugins.tooltip.enabled = false;
Chart.defaults.plugins.tooltip.mode = 'index';
Chart.defaults.plugins.tooltip.position = 'nearest';
Chart.defaults.plugins.tooltip.external = coreui.ChartJS.customTooltips;
Chart.defaults.defaultFontColor = '#646470';
const random = (min, max) =>
// eslint-disable-next-line no-mixed-operators
Math.floor(Math.random() * (max - min + 1) + min);




// // eslint-disable-next-line no-unused-vars
// const mainChart = new Chart(document.getElementById('main-chart'), {
//   type: 'pie',
//   data: {
//     labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
//     datasets: [{
//       label: 'My First dataset',
//       backgroundColor: coreui.Utils.hexToRgba(coreui.Utils.getStyle('--cui-info'), 10),
//       borderColor: coreui.Utils.getStyle('--cui-info'),
//       pointHoverBackgroundColor: '#fff',
//       borderWidth: 2,
//       data: [random(50, 200), random(50, 200), random(50, 200), random(50, 200), random(50, 200), random(50, 200), random(50, 200)],
//       fill: true
//     }, {
//       label: 'My Second dataset',
//       borderColor: coreui.Utils.getStyle('--cui-success'),
//       pointHoverBackgroundColor: '#fff',
//       borderWidth: 2,
//       data: [random(50, 200), random(50, 200), random(50, 200), random(50, 200), random(50, 200), random(50, 200), random(50, 200)]
//     }, {
//       label: 'My Third dataset',
//       borderColor: coreui.Utils.getStyle('--cui-danger'),
//       pointHoverBackgroundColor: '#fff',
//       borderWidth: 1,
//       borderDash: [8, 5],
//       data: [65, 65, 65, 65, 65, 65, 65]
//     }]
//   },
//   options: {
//     maintainAspectRatio: false,
//     plugins: {
//       legend: {
//         display: false
//       }
//     },
//     scales: {
//       x: {
//         grid: {
//           drawOnChartArea: false
//         }
//       },
//       y: {
//         ticks: {
//           beginAtZero: true,
//           maxTicksLimit: 5,
//           stepSize: Math.ceil(250 / 5),
//           max: 250
//         }
//       }
//     },
//     elements: {
//       line: {
//         tension: 0.4
//       },
//       point: {
//         radius: 0,
//         hitRadius: 10,
//         hoverRadius: 4,
//         hoverBorderWidth: 3
//       }
//     }
//   }
// });
//# sourceMappingURL=main.js.map




function getDashboardSalesData(){
  $.ajax({
    type: "GET",
    url: "api/dashboard/data/sales",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
    success: (data) => {
      if (data.status === "success") {
          setChartSalesData(data.data)
      } else {
        console.log(data);
    }
      
  },
  error: (xhr, status, error) => {
      // Display the error message on the page
      console.log("error");
      console.log(error);
  }
});
}
function getDashboardProduct2SalesData(){
  $.ajax({
    type: "GET",
    url: "api/dashboard/data/product2sales",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
    success: (data) => {
      if (data.status === "success") {
          setDashboardProduct2SalesData(data.data)
      } else {
        console.log(data);
    }
      
  },
  error: (xhr, status, error) => {
      // Display the error message on the page
      console.log("error");
      console.log(error);
  }
});
}






function setChartSalesData(data)
{
  const salesChart = document.getElementById('sales-chart');
  const labels = Object.keys(data);
  const datasetData = Object.values(data);
  new Chart(salesChart, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: datasetData,
        backgroundColor:['#ABEBC6','#AED6F1','#F5B7B1','#FCF3CF','#F6DDCC','#D5D8DC'],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function setDashboardProduct2SalesData(data)
{
 
  const topProductsChart = document.getElementById('top-products-sale');
  const labels = Object.keys(data);
  const datasetData = Object.values(data);

  new Chart(topProductsChart, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'No Of Sales vs Products',
        data: datasetData,
        backgroundColor:['#ABEBC6','#AED6F1','#F5B7B1','#FCF3CF','#F6DDCC','#D5D8DC','#EDBB99','#CD6155','#5D6D7E','#1ABC9C','#BB8FCE'],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  }
  );

}