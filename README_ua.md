* **[Change to english](README.md)**

# Web_World: Park-Auto <a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/images/web_logo.jpg" width="40px" style="border: 10px solid orange;"></a>
Фінальний проект курсу Python 19 Data Science, на основі веб-фреймворку - Django.

За допомогою цієї програми ви зможете автоматично ідентифікувати реєстраційні номери автомобілів на зображеннях, відстежувати тривалість паркування для кожного окремого автомобіля та розраховувати накопичену вартість паркування.
Парковка – це не просто місце для вашого автомобіля, це важлива частина міської інфраструктури, яка впливає на комфорт і безпеку всіх учасників дорожнього руху.
Кожен раз, коли ви обираєте місце для паркування, думайте про те, як ваше рішення вплине на інших. Залиште достатньо місця для пішоходів, велосипедистів та інших водіїв. Належне паркування – це повага до інших та внесок у створення безпечнішого та зручнішого міста.


## Table of contents:
   * [General info](#general-info)
   * [Features](#features)
   * [Image recognizing](#image-recognizing)  
   * [Setup-Local](#setup-locally)
   * [Setup-Docker](#docker-setup)
   * [Technologies](#technologies)

## Основна інформація:
**Web_World: Park-Auto** - працює на основі наступних алгоритмів:
* **[paddleocr](https://github.com/PaddlePaddle/PaddleOCR/blob/main/README_en.md)** - допомагає створювати багатомовні, провідні та практичні інструменти оптичного розпізнавання символів, які допомагають користувачам тренувати кращі моделі та застосовувати їх на практиці.
* **[opencv](https://github.com/opencv/opencv?tab=readme-ov-file)** - відкрита бібліотека комп’ютерного бачення.

## Особливості проекта:
**Web_World: Park-Auto** - надає наступні функції:
* 👨‍💻 **Авторизація та автентифікація:** - користувачі можуть реєструватися, входити та виходити з власного профіля.
* 🚗 **Завантаження зображень:** - користувачі можуть завантажувати зображення для розпізнавання номерів автомобіля через особистий профіль.
* 🤓 **Керування профілем користувача:** - історія автомобіля, розпізнані номери, історія платежів.
* 😎 **Керування профілем адміністратора** - налаштований профіль адміністратора django, що дає повну можливість керування проектом.
* 📆 **Celery планувальник завдань** - планувальник завдань, який виконує автоматичні сповіщення електронною поштою для користувачів із чорного списку.
* 🌌 **Алгоритм моделі: [paddleocr](https://huggingface.co/spaces/itsyoboieltr/anpr/blob/main/ANPR.ipynb)** - алгоритм розпізнавання вже навчений і впроваджений.
* 🐳 **Докер-контейнер:** - проект можна запустити через докер контейнер.

## Image recognizing:
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl1.jpg" width="540px" style="border: 10px solid orange;"></a>
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl2.jpg" width="540px" style="border: 10px solid orange;"></a>
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl3.jpg" width="540px" style="border: 10px solid orange;"></a>
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl4.jpg" width="540px" style="border: 10px solid orange;"></a>

## Розгорнути локально:
1. Перший крок до виконання - клонування репозиторія:

```sh
git clone -b main https://github.com/IVadymMarchenko/web_world.git
```

2. Другий крок активувати віртуальне середовище та встановлення залежностей з кореневої папки де знаходиься pyproject.toml:

```sh
poetry shell
```
```sh
poetry install --no-root
```

3. Після встановлення залежностей:

    * Створюємо .env файл в кореневій папці та заповнюємо його наступною інформацією:
```sh
DJANGO_SECRET_KEY=*your secret key*

POSTGRES_DB_NAME=*your postgre db name*
POSTGRES_USER=postgres
POSTGRES_PASSWORD=w*your postgre db password*
POSTGRES_PORT=5432
POSTGRES_DOMAIN=*your postgre domain*

EMAIL_HOST=*your main smtp*
EMAIL_PORT=*your main smtp port*
EMAIL_HOST_USER=*your email address*
EMAIL_HOST_PASSWORD=*your email password*

CLOUD_NAME=*your cloudidnary name*
API_KEY=*your cloudinary api key*
API_SECRET=*your api secret phrase*

REDIS_HOST0=*your redis host for celery*/0
REDIS_HOST1=*your redis host for celery*/1
```

4. Після чого запускаємо докер контейнер та виконуємо міграції для бази даних:
    * Run postgre docker container.
    * Run redis docker container.
        - з любого системного термінала виконайте команди:
          
Для postgre:
```sh
docker run --name postg_data_science -d -h localhost -p 5432:5432 -u postgres -e POSTGRES_PASSWORD=*your password from env file POSTGRES_PASSWORD* postgres
```

Для redis:
```sh
docker run --name my-redis -d -p 6379:6379 redis
```

Переходимо на рівень нижче в /app_parking/ та виконуємо міграції:
```sh
(env)$> cd app_parking
(env)$app_parking> python manage.py makemigrations
(env)$app_parking> python manage.py migrate
```

5. Перед запуском сервера запускаємо celery worker та beat команди в різних терміналах:
    * Run celery worker commdand.
    * Run celery beat command.
    * Run web server.
        - З папки /app_parking/:

```sh
(env)$> cd app_parking
```
 
Перший тернмінал - для celery worker команди:
```sh
(env)$app_parking> celery -A app_parking worker -l info -P eventlet
```

Другий термінал - для celery beat команди:
```sh
(env)$app_parking> celery -A app_parking beat -l info
```

Третій термінал - для запуску сервера:
```sh
(env)$app_parking> py manage.py runserver  
```

* Відвідайте `http://127.0.0.1:8000/.

## Розгорнути в контейнері:
З кореневої папки виконайте команду:
1. Створюємо контейнер через `docker-compose`:

    ```sh
    docker-compose build
    ```

2. Запускаємо контейнер:

    ```sh
    docker-compose up
    ```

3. Відкриваємо `http://localhost:8000` в браузері.


## Технології:
Project is mainly based on:
* 🐍 **Python** - серверна мова програмування.
* 🌠 **HTML/CSS/JavaScript:** - інтерфейсні мови програмування.
* 🤠 **Django** -  веб-фреймворк python.
* 🌌 **Paddleocr / OpenCV** - моделі розпізнавання номерних знаків.
* 🐘 **PostgreSQL** - об'єктно-реляційна система управління базами даних.
* ⚙️ **Redis** - база даних, що відповідає за зберігання і кеш основної бази даних.
* 📆 **Celery** - автоматизований планувальник завдань.
* 🐳 **Docker** - програмна платформа для швидкої розробки, тестування та розгортання програм.
* 👀 **GitHub** - зберігання, відстеження та співпраця над розробкою/розгортанням проекту.
* 🎰 **Googleapis** - сервіс від Google, який надає різноманітну колекцію веб-шрифтів.
* 🌎 **Koyeb** - платформа для розгортання проекту.
* 👨‍👦‍👦 **Trello** - візуальний інструмент, який дозволяє вашій команді керувати проектами, робочими процесами та будь-яким видом роботи.