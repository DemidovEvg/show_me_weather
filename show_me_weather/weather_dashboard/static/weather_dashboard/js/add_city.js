const addCity = document.getElementById('add_city');
addCity.addEventListener('click', (event) => addCityModal(event));

function addCityModal(event) {
    // Изменяем заголовок, кнопку submit
    const CityModalLabel = document.getElementById('CityModalLabel');
    CityModalLabel.textContent = "Добавить город";
    const citySubmit = document.getElementById('citySubmit');
    citySubmit.textContent = "Добавить";
    const cityNameInput = document.querySelector('#CityModal #id_name');
    cityNameInput.value = '';
    cityNameInput.readOnly = false;

    // Изменяем действие для формы
    const formCity = document.getElementById('form_city');
    formCity.action = `create/city`;
}