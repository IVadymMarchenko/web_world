* **[Change to ukrainian](README_ua.md)**

# Web_World: Park-Auto <a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/images/web_logo.jpg" width="40px" style="border: 10px solid orange;"></a>
The final project of the course Python 19 Data Science, on the Web framework - Django.

With this application, you will be able to automatically identify car registration numbers in images, track the length of parking for each unique car, and calculate accumulated parking costs.
Parking is not just a place for your car, it is an important part of the city infrastructure that affects the comfort and safety of all road users. 
Every time you choose a parking place, think about how your decision will affect others. Leave enough space for pedestrians, cyclists and other drivers. Proper parking is respect for others and a contribution to creating a safer and more convenient city.


## Table of contents:
   * [General info](#general-info)
   * [Features](#features)
   * [Image recognizing](#image-recognizing)  
   * [Setup-Local](#setup-locally)
   * [Setup-Docker](#docker-setup)
   * [Technologies](#technologies)

## General info:
**Web_World: Park-Auto** - it performs the following algorithm model:
* **[paddleocr](https://github.com/PaddlePaddle/PaddleOCR/blob/main/README_en.md)** - aims to create multilingual, awesome, leading, and practical OCR tools that help users train better models and apply them into practice.
* **[opencv](https://github.com/opencv/opencv?tab=readme-ov-file)** - open Source Computer Vision Library

## Features:
**Web_World: Park-Auto** - performs the following features:
* 👨‍💻 **Authorization and Authentication:** - users can register, log in, and log out.
* 🚗 **Image Uploading:** - users can upload images for car number recognition via personal profile.
* 🤓 **User profile management:** - car auto history, recognized numbers, payment history.
* 😎 **Admin profile management** - adjusted django admin profile, giving full project management possibility.
* 📆 **Celery task scheduler** - task scheduler that performs auto email notifications, for blacklisted users.
* 🌌 **Model algorithm: [paddleocr](https://huggingface.co/spaces/itsyoboieltr/anpr/blob/main/ANPR.ipynb)** - recognition algorithm already trained and implemented.
* 🐳 **Docker container:** - the project can start-up via containerized Docker.

## Image recognizing:
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl1.jpg" width="540px" style="border: 10px solid orange;"></a>
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl2.jpg" width="540px" style="border: 10px solid orange;"></a>
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl3.jpg" width="540px" style="border: 10px solid orange;"></a>
<a><img src="https://github.com/IVadymMarchenko/web_world/blob/main/app_parking/app_home/images/about_project/exmp/exmpl4.jpg" width="540px" style="border: 10px solid orange;"></a>

## Setup-Locally:
1. The first thing to do is to clone the repository:

```sh
git clone -b main https://github.com/IVadymMarchenko/web_world.git
```

2. Activate virtual environment and install dependencies from the root folder where pyproject.toml exists:

```sh
poetry shell
```
```sh
poetry install --no-root
```

3. Once `poetry` has finished downloading the dependencies:

    * Create .env file in project root and fill in the file like this example:
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

4. Then run docker container and make migrations for db:
    * Run postgre docker container.
    * Run redis docker container.
        - From any terminal window:
          
For postgre:
```sh
docker run --name postg_data_science -d -h localhost -p 5432:5432 -u postgres -e POSTGRES_PASSWORD=*your password from env file POSTGRES_PASSWORD* postgres
```

For redis:
```sh
docker run --name my-redis -d -p 6379:6379 redis
```

From root projectfolder /app_parking/ make migrations:
```sh
(env)$> cd app_parking
(env)$app_parking> python manage.py makemigrations
(env)$app_parking> python manage.py migrate
```

5. Before server start-up run celery worker and beat commands in separate terminals:
    * Run celery worker commdand.
    * Run celery beat command.
    * Run web server.
        - From project folder /app_parking/:

```sh
(env)$> cd app_parking
```
 
First terminal window - for celery worker commdand:
```sh
(env)$app_parking> celery -A app_parking worker -l info -P eventlet
```

Second terminal window - for celery beat commdand:
```sh
(env)$app_parking> celery -A app_parking beat -l info
```

Third terminal window - for web server start-up:
```sh
(env)$app_parking> py manage.py runserver  
```

* And navigate to `http://127.0.0.1:8000/.

## Docker-setup:
From the root folder:
1. Build containers via `docker-compose`:

    ```sh
    docker-compose build
    ```

2. Start containers:

    ```sh
    docker-compose up
    ```

3. Open `http://localhost:8000` in a browser.

## Technologies:
Project is mainly based on:
* 🐍 **Python** - backend programming language.
* 🌠 **HTML/CSS/JavaScript:** - frontend programming languages.
* 🤠 **Django** -  python web framework.
* 🌌 **Paddleocr / OpenCV** - vision image recognition models.
* 🐘 **PostgreSQL** - object-relational database management system.
* ⚙️ **Redis** - data base that is responsible for the storage and cache of the main database.
* 📆 **Celery** - automation task scheduler.
* 🐳 **Docker** - a software platform for rapid application development, testing and deployment.
* 👀 **GitHub** - storing, tracking, and collaborating on project development/deployment.
* 🎰 **Googleapis** - a service by Google that provides a diverse collection of web fonts.
* 🌎 **Koyeb** - service for project deplotment.
* 👨‍👦‍👦 **Trello** - a visual tool that allows your team to manage projects, workflows and any type of job.