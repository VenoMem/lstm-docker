var refreshInterval;

/**
 * Wymiana danych front-backend
 * **/
function dataExchange(jsonData = {}) {

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
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
    stopRefresh();
    var streamData = document.getElementById('stream-data').value;

    var scheduleOption = document.getElementById("schedule").value;
    if (scheduleOption === "hourly") {
        // dataExchange();
        // refreshInterval = setInterval(dataExchange, 3600000); // 3600000 milisekund = 1 godzina
    }

    //TODO: get data from server
    let jsonMetrics = {"r2": 0.85, "rmse": 0.12, "mape": 0.08};


    plottingChart(jsonMetrics, 'bar-chart');
    actualizeMetrics(jsonMetrics)

}

function stopRefresh() {
    clearInterval(refreshInterval);
}

document.getElementById("schedule").addEventListener("change", visualizations);


visualizations()


