let citySetForGraph = document.getElementById('form_graphic');
citySetForGraph.addEventListener('change', (event) => reloadGraph(event));

const ctx = document.getElementById('myChart').getContext('2d');

function reloadGraph(event) {
    let input = event.target.closest('input[class="city"]');

    let dateFrom = document.querySelector('#form_graphic #id_graphic_date_from')?.value;
    let dateTo = document.querySelector('#form_graphic #id_graphic_date_to')?.value;

    const citySet = []
    for (let input of document.querySelectorAll('#city_set_for_graph .city')) {
        if (input.checked) {
            citySet.push(input.value)
        }
    }

    if (!citySet.length) {
        if (chartObj.isChartExist()) {
            chartObj.destroy();
        }
        return;

    };

    let apiCityWeatherUrl = document.getElementById('city_set_for_graph').dataset.apiCityWeatherUrl;
    let promis = getCityData(apiCityWeatherUrl, citySet, dateFrom, dateTo);

    // Обработаем данные и запишем в дату
    promis.then(data => {
        // console.log(data);
        let datasets = []
        for (let city of Object.entries(data)) {
            let cityName = city[1].name;
            let r = Math.floor(Math.random() * 200);
            let g = Math.floor(Math.random() * 200);
            let b = Math.floor(Math.random() * 200);

            let color = `rgb(${r}, ${g}, ${b})`;
            let data = [];
            for (let weather of Object.entries(city[1].weather_set)) {
                let hour = `0${weather[1].hour}`.slice(-2,);
                let newDate = Date.parse(`${weather[1].date}T${hour}:00:00`);

                data.push({
                    x: newDate,
                    y: weather[1].temperature,
                });
            }
            if (data.length) {
                datasets.push({
                    label: cityName,
                    borderColor: color,
                    data: data,
                    borderWidth: 1,
                    fill: false,
                    // tension: 0.1
                });
            }
        }

        let options = {
            plugins: {
                title: {
                    text: 'График погоды',
                    display: true
                }
            },
            scales: {
                x: {
                    type: 'time',
                    distribution: 'linear',
                    // unitStepSize: 1,
                    format: "YYYY-MM-DD HH:mm:ss",
                    time: {
                        displayFormats: {
                            'day': 'dd.MM.yy',
                            'week': 'DD.MM',
                            'month': 'DD.MM',
                            'year': 'MMMM'
                        },
                        unit: 'day',
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Температура'
                    }
                }
            },
        };

        const config = {
            type: 'line',
            data: { datasets: datasets },
            options: options
        };

        if (chartObj.isChartExist()) {
            chartObj.destroy();
        }
        const chart = chartObj.createChart(ctx, config);

    })
}

function getCityData(apiCityWeatherUrl, citySet, dateFrom, dateTo) {
    let paramsObj = {};
    for (let num in citySet) {
        paramsObj['city_' + num] = citySet[num];
    }
    if (dateFrom) {
        paramsObj['date_from'] = dateFrom;
    }

    if (dateTo) {
        paramsObj['date_to'] = dateTo;
    }

    let params = new URLSearchParams(paramsObj)
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let csrftoken = getCookie('csrftoken');

    const init = {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
    };

    const protocol = window.location.protocol;
    let baseUrl = protocol + '//' + window.location.host

    const url = new URL(apiCityWeatherUrl, baseUrl);
    let responseData = null;
    ///////////////////////////////////////////////////////////////
    let promis = fetch(url + '?' + params, init)
        .then(response => {

            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => alert(error));
    return promis;
}


let chartObj = {
    myChart: null,
    createChart(ctx, config) {
        this.myChart = new Chart(ctx, config);
        return this.myChart;
    },
    getChart() {
        return this.myChart;
    },
    isChartExist() {
        return Boolean(this.myChart);
    },
    destroy() {
        this.myChart.destroy();
    }
}