const editCity = document.getElementById('edit_city');
editCity.addEventListener('click', (event) => editCityModal(event));

function editCityModal(event) {
    // Синхронизируем изменяемое значение
    const cityOptions = document.querySelectorAll('#id_city option');
    let selectedCityValue = null;
    let selectedCityPk = null;

    for (let option of cityOptions) {
        if (option.selected) {
            selectedCityValue = option.textContent;
            selectedCityPk = option.value;
            if (!option.value) {
                document.getElementById('citySubmit').style.display = 'none';
            } else {
                document.getElementById('citySubmit').style.display = 'block';
            }
        }
    }
    const cityEditUrl = `update/city/${selectedCityPk}`;
    syncCityModal(cityEditUrl, selectedCityValue);
}

function syncCityModal(cityEditUrl, selectedCityValue) {
    // Изменяем заголовок, кнопку submit
    const CityModalLabel = document.getElementById('CityModalLabel');
    CityModalLabel.textContent = "Изменить город";
    const citySubmit = document.getElementById('citySubmit');
    citySubmit.textContent = "Изменить";
    const cityNameInput = document.querySelector('#CityModal #id_name');
    cityNameInput.value = selectedCityValue;
    cityNameInput.readOnly = false;

    // Изменяем действие для формы
    const formCity = document.getElementById('form_city');
    formCity.action = cityEditUrl;
}