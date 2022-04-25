const deleteWeather = document.getElementById('weather_table');

if (deleteWeather) {
    deleteWeather.addEventListener('click', (event) => deleteWeatherModal(event));
}


function deleteWeatherModal(event) {
    // Определяем строку
    // Делаем запрос на сервер что бы вызрузить данные данной погоды
    let img = event.target.closest('img');
    if (!img) return;
    if (!img.classList.contains('delete_weather')) return;

    let editButton = img;
    const weatherDeleteUrl = editButton.dataset.weatherDeleteUrl;
    let promis = getWeather(weatherDeleteUrl);

    promis.then(weather => {
        function insertValueAndDisable(selector, value) {
            const element = document.querySelector(selector);
            if (value) {
                element.value = value;
            }
            element.disabled = true;
            element.readOnly = true;
        }

        insertValueAndDisable('#id_temperature', weather.temperature);
        insertValueAndDisable('#id_date', weather.date);
        insertValueAndDisable('#id_hour', weather.hour);

        for (let option of document.querySelectorAll('#id_city option')) {
            option.selected = false;
            if (option.textContent == weather.city.name) {
                option.selected = true;
            }
        }
        insertValueAndDisable('#id_city', null);

        for (let option of document.querySelectorAll('#id_weather option')) {
            option.selected = false;
            if (option.textContent == weather.weather) {
                option.selected = true;
            }
        }
        insertValueAndDisable('#id_weather', null);
    }
    );

    // Изменяем заголовок, кнопку submit
    const weatherModalLabel = document.getElementById('WeatherModalLabel');
    weatherModalLabel.textContent = "Удалить погоду";
    const weatherSubmit = document.getElementById('weatherSubmit');
    weatherSubmit.textContent = "Удалить";

    // Изменяем действие для формы
    const formWeather = document.getElementById('form_weather');
    formWeather.action = weatherDeleteUrl;

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