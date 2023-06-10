/**
 * Rysowanie wykresów
 * metrics - słownik metryk
 * type (str) - typ wykresu
 *
 * **/
function plottingChart(metrics, type) {

    // var metrics = JSON.parse(metrics);

    console.log(Object.keys(metrics), Object.values(metrics))
    var barChartCanvas = document.createElement('canvas');
    barChartCanvas.id = type;
    document.getElementById('chart-container').appendChild(barChartCanvas);

    var barChart = new Chart(barChartCanvas, {
        type: 'bar',
        data: {
            labels: Object.keys(metrics),
            datasets: [{
                label: 'Metryki',
                data: Object.values(metrics),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

}


/**
 * Aktualizacja metryk na froncie
 * jsonMetrics - słownik metryk

 * **/

function actualizeMetrics(jsonMetrics = {}) {


    var container = document.getElementById('results-container');

    console.log(container)
    for (var key in jsonMetrics) {
        if (jsonMetrics.hasOwnProperty(key)) {
            var div = document.createElement('div');
            div.classList.add('result-item');
                console.log(key, )
            var label = document.createElement('label');
            label.textContent = key.charAt(0).toUpperCase() + key.slice(1) + ":";

            var span = document.createElement('span');
            span.id = key;
            span.textContent = jsonMetrics[key].toFixed(2);

            div.appendChild(label);
            div.appendChild(span);

            container.appendChild(div);
        }
    }
}