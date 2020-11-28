var ctx = document.getElementById("readingsChart");

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'second'
                },
                distribution: 'series'
            }]
        },
        plugins: {
            zoom: {
                zoom: {
                    enabled: true,
                    mode: 'x',

                    rangeMin: {
                        x: null,
                        y: null,
                    },
                    rangeMax: {
                        x: null,
                        y: null,
                    },
                    speed: 0.1,
                    threshold: 2,
                    sensitivity: 3,
                    onZoom: function({ chart }) { console.log("Zooming !!"); },
                },
                pan: {
                    enabled: true,
                    mode: 'x',

                    speed: 20,
                    threshold: 10,
                    rangeMin: {
                        x: null,
                        y: null,
                    },
                    rangeMax: {
                        x: null,
                        y: null,
                    },

                    onPan: function({ chart }) { console.log("Panning"); },
                }
            },

            // pan: {
            //     enabled: true,
            //     mode: 'xy',
            // },
            // zoom: {
            //     zoom: {
            //         enabled: true,
            //         mode: 'x',
            //     }
            // }
        }
    }
});

function addDataset(chart, label, data) {
    chart.data.datasets.push({
        data: data,
        label: label,
        borderColor: "#3e95cd",
        fill: false
    })
    chart.update()
}

function addSample(chart, sample, label, x_label) {

    for (var i = 0; i < chart.data.datasets.length; i++) {
        if (chart.data.datasets[i].label === label) {
            chart.data.datasets[i].data.push(sample)
            chart.data.labels.push(x_label)
            break;
        }
    }
    chart.update();
}

function getReadings(sensor_name, period, onDone) {
    $.get("/api/sensors/" + sensor_name + "/readings", {
            "dateFrom": period.begin,
            "dateTo": period.end
        })
        .done(function(response) {
            console.log(response.readings)
            onDone(response)
        })
        .fail(function() {
            console.log("getting new data failed")
        })
}

function updateChart(response) {
    for (i = 0; i < response.readings.length; i++) {
        addSample(chart, response.readings[i].value, label,
            response.readings[i].timestamp)
    }
}

/* Note: sensor_name, label, period come from html template */
addDataset(chart, label, [])
getReadings(sensor_name, initialPeriod, updateChart)