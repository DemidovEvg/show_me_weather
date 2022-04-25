const editWeatherTable = document.getElementById('weather_table');

if (editWeatherTable) {
    editWeatherTable.addEventListener('click', (event) => editWeatherModal(event));
}

function editWeatherModal(event) {
    // Определяем строку
    // Делаем запрос на сервер что бы вызрузить данные данной погоды
    let img = event.target.closest('img');
    if (!img) return;
    if (!img.classList.contains('edit_weather')) return;

    let editButton = img;
    const weatherEditUrl = editButton.dataset.weatherEditUrl;
    syncWeatherModal(weatherEditUrl);
}

function syncWeatherModal(weatherEditUrl) {
    let promis = getWeather(weatherEditUrl);

    promis.then(weather => {
        document.getElementById('id_temperature').value = weather.temperature;
        document.getElementById('id_date').value = weather.date;
        document.getElementById('id_hour').value = weather.hour;

        for (let option of document.querySelectorAll('#id_city option')) {
            option.selected = false;
            if (option.textContent == weather.city.name) {
                option.selected = true;
            }
        }

        for (let option of document.querySelectorAll('#id_weather option')) {
            option.selected = false;
            if (option.textContent == weather.weather) {
                option.selected = true;
            }
        }
    }
    );

    // Изменяем заголовок, кнопку submit
    const weatherModalLabel = document.getElementById('WeatherModalLabel');
    weatherModalLabel.textContent = "Изменить погоду";
    const weatherSubmit = document.getElementById('weatherSubmit');
    weatherSubmit.textContent = "Изменить";

    // Изменяем действие для формы
    const formWeather = document.getElementById('form_weather');
    formWeather.action = weatherEditUrl;
}

function getWeather(weatherEditUrl) {
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

    const url = new URL(weatherEditUrl, baseUrl);
    let responseData = null;
    ///////////////////////////////////////////////////////////////
    let promis = fetch(url, init)
        .then(response => {

            return response.json();
        })
        .then(data => {
            return data
        })
        .catch(error => alert(error));
    return promis;
}