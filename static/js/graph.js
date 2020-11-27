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
    $.get("/api/sensors/" + sensor_name + "/readings", {})
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

/* Note: sensor_name and label come from html template */
addDataset(chart, label, [])
getReadings(sensor_name, "", updateChart)