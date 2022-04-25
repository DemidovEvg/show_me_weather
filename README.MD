- Установка python зависимостей:
pip install -r requirements.txt

- Установить node js + npm

- Установка js зависимостей:
В директории с файлом package-lock.json вызвать команду:
npm install
При этом создастся папка node_modules с зависимости

- Сборка статических файлов:
python manage.py collecstatic 
При этом берутся статика из папки приложения + зависимости из node_modules чере django_node_assets