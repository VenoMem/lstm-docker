var refreshInterval;


/** Czyszczenie danych po załadowaniu nowego formsa **/
function clearingChartSpace() {

    let chartContainer = document.getElementById('chart-container')
    chartContainer.innerHTML = '';


    var container = document.getElementById("results-container");
    container.innerHTML = "";
}

/**
 * Wymiana danych front-backend
 * **/

function dataExchange(jsonData = {}, method = "GET") {

    var xhr = new XMLHttpRequest();
    xhr.open(method, "/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response.message);
        }
    };
    xhr.send(JSON.stringify(jsonData));

}

/**
 * Uruchamianie wszystkich akcji dotyczących wizualizacji - wyniki i wykresy
 *
 * Możliwość odświeżania danych co godzinę i aktualizacja statystyk.
 * Możliwość też wklejenia url danych strumieniowych (raczej niepotrzebne?)
 * **/

function visualizations() {
    var resultDiv = document.getElementById('result');
    var pred = resultDiv.dataset.pred;
    var hours = resultDiv.dataset.hours;
    var stats = resultDiv.dataset.stats;

    let pred_from_hours = {
        "hours": hours,
        "pred": pred
    }
    console.log(stats, pred_from_hours)

    var selectElement = document.getElementById('command');
    var resultElement = document.getElementById('result');


    var scheduleOption = document.getElementById("schedule").value;

    if (scheduleOption === "hourly") {

        console.log(scheduleOption)
        refreshInterval = setInterval(visualizations, 3600000); // 3600000 milisekund = 1 godzina
    } else {
        stopRefresh();
    }

    selectElement.addEventListener('change', function () {
        var selectedOption = selectElement.value;
        if (selectedOption == 'learn') {
            resultElement.textContent = 'Metryki: ' + JSON.stringify(stats, null, 2);
            // clearingChartSpace();

        } else {
            clearingChartSpace()
            // plottingChart(pred_from_hours, 'line');

            var start = document.getElementById("start-input").value;
            var end = document.getElementById("end-input").value;
            chartGenerator('line', pred_from_hours, start, end);
        }

    });

    // plottingChart(data, 'scatter');
    // plottingChart(jsonMetrics, 'bar');
    


}

function stopRefresh() {
    clearInterval(refreshInterval);
}







