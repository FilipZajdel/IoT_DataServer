var ctx = document.getElementById("readingsChart");

var samples = {};
var axisLimits = {
    xmin: 0,
    xmax: 0,
    xcache: 7200000
};
var duringDataUpdate = false

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        scales: {
            xAxes: [{
                id: 'time-axis',
                type: 'time',
                time: {
                    unit: 'minute'
                },
                beforeUpdate: function(evt) {
                    if (isOlderDataNeeded(evt.min) && !duringDataUpdate) {
                        console.log("Older data needed!")
                        var beginDate = new Date(lastUpdatedPeriod.begin)
                        beginDate.setHours(beginDate.getHours() - 2)

                        lastUpdatedPeriod.end = lastUpdatedPeriod.begin
                        lastUpdatedPeriod.begin = beginDate.toISOString()

                        getReadings(sensor_name, lastUpdatedPeriod,
                            updateSamplesAndChart)
                    } else {
                        console.log("Older data not needed!")
                    }
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

function addSamples(new_samples, dates) {
    for (var i = 0; i < new_samples.length; i++) {
        samples[dates[i]] = new_samples[i]
    }

    console.log(samples)
}

function getSortedSamplesKeys() {
    var keys = [...Object.keys(samples)]
    keys.sort(compareDates)

    console.log(keys)
    return keys
}

function getReadings(sensor_name, period, onDone) {
    duringDataUpdate = true

    $.get("/api/sensors/" + sensor_name + "/readings", {
            "dateFrom": period.begin,
            "dateTo": period.end
        })
        .done(function(response) {
            console.log(response.readings)
            onDone(response)
            duringDataUpdate = false
        })
        .fail(function() {
            console.log("getting new data failed")
            duringDataUpdate = false
        })
}

function updateSamplesAndChart(response) {

    var new_samples = []
    var timestamps = []
    var sorted_keys = []

    for (var i = 0; i < response.readings.length; i++) {
        new_samples.push(response.readings[i].value)
        timestamps.push(response.readings[i].timestamp)
    }

    addSamples(new_samples, timestamps)
    sorted_keys = getSortedSamplesKeys()

    chart.data.datasets[0].data = []

    for (var i = 0; i < sorted_keys.length; i++) {
        chart.data.datasets[0].data.push(samples[sorted_keys[i]])
    }

    chart.data.labels = [...sorted_keys];

    axisLimits.xmin = (new Date(sorted_keys[0])).valueOf()
    chart.update()
}

function compareDates(dateA, dateB) {
    return (new Date(dateA)) - (new Date(dateB))
}

function isOlderDataNeeded(minX) {
    return ((minX - axisLimits.xcache) < axisLimits.xmin)
}

function isNewerDataNeeded(chart) {
    /* TODO: It was no purpose to use it, because chart is updated backwards */
    return false
}

/* Note: sensor_name, label, period come from html template */
addDataset(chart, label, [])
getReadings(sensor_name, lastUpdatedPeriod, updateSamplesAndChart)