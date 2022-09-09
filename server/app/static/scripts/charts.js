let tsDelta = 3 * 60 * 60 * 1000;

document.querySelector("#date-select-1m")
.addEventListener('click', function(e) {
  tsDelta = 60 * 1000;
});

document.querySelector("#date-select-5m")
.addEventListener('click', function(e) {
  tsDelta = 5 * 60 * 1000;
});

document.querySelector("#date-select-1h")
.addEventListener('click', function(e) {
  tsDelta = 60 * 60 * 1000;
});

document.querySelector("#date-select-3h")
.addEventListener('click', function(e) {
  tsDelta = 3 * 60 * 60 * 1000;
});

async function fetchData(clientName, hardware, indicator, startIdx, endIdx) {
  let url = "http://127.0.0.1:5000/getData?clientName=" +
                       clientName + "&hardware=" +
                       hardware + "&indicator=" +
                       indicator + "&startIdx=" +
                       startIdx + "&endIdx=" +
                       endIdx

  let sensorsData = await fetch(url)
  .then(response => response.json())
  .then(jsonData => jsonData.data);

  return sensorsData;
}

async function fetchDataIncr(clientName, hardware, indicator, startScore, endScore) {
  let url = "http://127.0.0.1:5000/getDataIncr?clientName=" +
                       clientName + "&hardware=" +
                       hardware + "&indicator=" +
                       indicator + "&startScore=" +
                       startScore + "&endScore=" +
                       endScore

  let sensorsData = await fetch(url)
  .then(response => response.json())
  .then(jsonData => jsonData.data);

  return sensorsData;
}

let gpu_data_total = await fetchDataIncr("nick_pc", "GPU", "core_temperature", parseInt((Date.now() - 3 * 60 * 60 * 1000) / 1000), "+inf");
let maxTs = gpu_data_total[gpu_data_total.length - 1][0];

var options = {
  chart: {
    type: "area",
    id: "temperatures-time-series",
    height: "70%",
    stacked: true,
    zoom: {
      enabled: false
    }
  },
  series: [{
    name: 'GPU temperature',
    data: gpu_data_total
  }],
  xaxis: {
    type: "datetime",
    tooltip: {
          enabled: true
        }
  },
  stroke: {
    curve: 'smooth'
  },
  dataLabels: {
    enabled: false
  },
  tooltip: {
        x: {
          format: "dd MMM yyyy HH:mm:ss"
        },
      },
}

var chart = new ApexCharts(document.querySelector("#first-graph"), options);

chart.render();

window.setInterval(async function () {
        let data = await fetchDataIncr("nick_pc", "GPU", "core_temperature", maxTs / 1000, "+inf");
        gpu_data_total = gpu_data_total.concat(data);
        maxTs = gpu_data_total[gpu_data_total.length - 1][0];
        let gpu_data = gpu_data_total.filter(rec => rec[0] >= maxTs - tsDelta);

        chart.updateSeries([{
          data: gpu_data
        }]);
      }, 1000);



let gpuMemData = await fetchData("nick_pc", "GPU", "memory", -1, -1);

var gauge_options_gpu_mem = {
  series: [gpuMemData[0][1]],
  chart: {
  height: "40%",
  type: 'radialBar',
  toolbar: {
    show: true
  },
  fontFamily: 'Fredoka, sans-serif'
},
plotOptions: {
  radialBar: {
    startAngle: -135,
    endAngle: 225,
     hollow: {
      margin: 0,
      size: '70%',
      background: '#fff',
      image: undefined,
      imageOffsetX: 0,
      imageOffsetY: 0,
      position: 'front',
      dropShadow: {
        enabled: true,
        top: 3,
        left: 0,
        blur: 4,
        opacity: 0.24
      }
    },
    track: {
      background: '#fff',
      strokeWidth: '67%',
      margin: 0,
      dropShadow: {
        enabled: true,
        top: -3,
        left: 0,
        blur: 4,
        opacity: 0.35
      }
    },

    dataLabels: {
      show: true,
      name: {
        offsetY: -10,
        show: true,
        color: '#888',
        fontSize: '17px'
      },
      value: {
        formatter: function(val) {
          return parseInt(val);
        },
        color: '#111',
        fontSize: '36px',
        show: true,
      }
    }
  }
},
fill: {
  type: 'gradient',
  gradient: {
    shade: 'dark',
    type: 'horizontal',
    shadeIntensity: 0.5,
    gradientToColors: ["#7f81d7", "#90e8e3"],
    inverseColors: true,
    opacityFrom: 1,
    opacityTo: 1,
    stops: [0, 100]
  }
},
stroke: {
  lineCap: 'round'
},
labels: ['Memory utilization'],
};

var gauge_chart_gpu_mem = new ApexCharts(document.querySelector("#second-graph"), gauge_options_gpu_mem);
gauge_chart_gpu_mem.render();

window.setInterval(async function () {
        let gpuMemData = await fetchData("nick_pc", "GPU", "memory", -1, -1);
        gauge_chart_gpu_mem.updateSeries([gpuMemData[0][1]]);
      }, 1000);


let gpuCoreData = await fetchData("nick_pc", "GPU", "core_load", -1, -1);

var gauge_options_gpu_core = {
  series: [gpuCoreData[0][1]],
  chart: {
  height: "40%",
  type: 'radialBar',
  toolbar: {
    show: true
  },
  fontFamily: 'Fredoka, sans-serif'
},
plotOptions: {
  radialBar: {
    startAngle: -135,
    endAngle: 225,
     hollow: {
      margin: 0,
      size: '70%',
      background: '#fff',
      image: undefined,
      imageOffsetX: 0,
      imageOffsetY: 0,
      position: 'front',
      dropShadow: {
        enabled: true,
        top: 3,
        left: 0,
        blur: 4,
        opacity: 0.24
      }
    },
    track: {
      background: '#fff',
      strokeWidth: '67%',
      margin: 0,
      dropShadow: {
        enabled: true,
        top: -3,
        left: 0,
        blur: 4,
        opacity: 0.35
      }
    },

    dataLabels: {
      show: true,
      name: {
        offsetY: -10,
        show: true,
        color: '#888',
        fontSize: '17px'
      },
      value: {
        formatter: function(val) {
          return parseInt(val);
        },
        color: '#111',
        fontSize: '36px',
        show: true,
      }
    }
  }
},
fill: {
  type: 'gradient',
  gradient: {
    shade: 'dark',
    type: 'horizontal',
    shadeIntensity: 0.5,
    gradientToColors: ["#7f81d7", "#90e8e3"],
    inverseColors: true,
    opacityFrom: 1,
    opacityTo: 1,
    stops: [0, 100]
  }
},
stroke: {
  lineCap: 'round'
},
labels: ['Cores utilization'],
};

var gauge_chart_gpu_core = new ApexCharts(document.querySelector("#third-graph"), gauge_options_gpu_core);
gauge_chart_gpu_core.render();

window.setInterval(async function () {
        let gpuCoreData = await fetchData("nick_pc", "GPU", "core_load", -1, -1);
        gauge_chart_gpu_core.updateSeries([gpuCoreData[0][1]]);
      }, 1000);


var tx_rx_options = {
  series: [{
  data: [128, 60]
}],
  chart: {
  type: 'bar',
  height: "40%",
  width: "80%",
  fontFamily: 'Fredoka, sans-serif'
},
plotOptions: {
  bar: {
    borderRadius: 15,
    horizontal: true,
  }
},
dataLabels: {
  enabled: true,
  style:{fontSize: "15px"}
},
xaxis: {
  categories: ['Tx', 'Rx'],
  labels: {style:{fontSize: "15px"}}
},
yaxis: {
  labels: {style:{fontSize: "15px"}}
}
};

var gauge_chart_gpu_txrx = new ApexCharts(document.querySelector("#fourth-graph"), tx_rx_options);
gauge_chart_gpu_txrx.render();

window.setInterval(async function () {
        let gpuTxData = await fetchData("nick_pc", "GPU", "pcie_tx", -1, -1);
        let gpuRxData = await fetchData("nick_pc", "GPU", "pcie_rx", -1, -1);
        gauge_chart_gpu_txrx.updateSeries([{
          data: [gpuTxData[0][1], gpuRxData[0][1]]
        }]);
      }, 1000);
