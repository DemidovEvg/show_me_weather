const deleteCity = document.getElementById('delete_city');
deleteCity.addEventListener('click', (event) => deleteCityModal(event));

function deleteCityModal(event) {
    // Синхронизируем удаляемое значение
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

    // Изменяем заголовок, кнопку submit
    const CityModalLabel = document.getElementById('CityModalLabel');
    CityModalLabel.textContent = "Удалить город";
    const citySubmit = document.getElementById('citySubmit');
    citySubmit.textContent = "Удалить";
    const cityNameInput = document.querySelector('#CityModal #id_name');
    cityNameInput.value = selectedCityValue;
    cityNameInput.readOnly = true;

    // Изменяем действие для формы
    const formCity = document.getElementById('form_city');
    formCity.action = `delete/city/${selectedCityPk}`;
}