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

function dataExchange(jsonData = {}, method="GET") {

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

    // var streamData = document.getElementById('stream-data').value;

    var scheduleOption = document.getElementById("schedule").value;
    let jsonMetrics = {"r2": 0.85, "rmse": 0.12, "mape": 0.08};
    jsonMetrics = dataExchange();
    jsonMetrics = {"r23343k": 0.85, "mksmclms": 0.12, "mape": 0.08};

    if (scheduleOption === "hourly") {
        jsonMetrics = {"r5": 0.85, "mksmclms": 0.12, "mape": 0.08};
        console.log(scheduleOption)
        refreshInterval = setInterval(visualizations, 3600000); // 3600000 milisekund = 1 godzina
    } else{
        stopRefresh();
    }

    //TODO : getting data  for predictions
    let data= [{
      x: -10,
      y: 0
    }, {
      x: 0,
      y: 10
    }, {
      x: 10,
      y: 5
    }, {
      x: 0.5,
      y: 5.5
    }];


    clearingChartSpace()
    plottingChart(jsonMetrics, 'line');
    plottingChart(data, 'scatter');
    plottingChart(jsonMetrics, 'bar');
    actualizeMetrics(jsonMetrics);


}

function stopRefresh() {
    clearInterval(refreshInterval);
}

// document.getElementById("schedule").addEventListener("change", visualizations);





