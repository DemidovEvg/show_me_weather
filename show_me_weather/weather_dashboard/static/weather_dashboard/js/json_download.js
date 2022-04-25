let formWeatherFilter = document.getElementById('form_weather_filter');

formWeatherFilter.addEventListener('change', (event) => syncDownloadLink(event));

function syncDownloadLink(event) {
    // Определяем значения фильтров
    let form = event.target.closest('form');
    if (!form) return;
    function addParams(paramsObj, key, value) {
        if (value) {
            paramsObj[key] = value;
        }
    }
    let paramsObj = {};

    addParams(paramsObj, 'date', form.querySelector('#id_date_filter').value)
    addParams(paramsObj, 'hour', form.querySelector('#id_hour_filter').value)

    let city = '';
    for (let option of form.querySelectorAll('#id_city_filter option')) {
        if (option.selected && option.value && option.textContent) {
            addParams(paramsObj, 'city', option.textContent)
        }
    }

    addParams(paramsObj, 'temperature', form.querySelector('#id_temperature_filter').value)

    let weather = '';
    for (let option of form.querySelectorAll('#id_weather_filter option')) {
        if (option.selected && option.value) {
            addParams(paramsObj, 'weather', option.value)
        }
    }

    console.log(paramsObj);

    let params = new URLSearchParams(paramsObj);

    let downloadJsonLink = document.getElementById('download-json');

    let url = new URL(downloadJsonLink.href);

    downloadJsonLink.href = url.pathname + '?' + params;






}