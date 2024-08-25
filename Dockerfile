# Use the official image of Python
FROM python:3.11

# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0

# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# RUN apt-get update && apt-get install libgl1

# RUN apt-get update && apt-get install -y python3-opencv
# RUN pip install opencv-python

# RUN pip install opencv-python-headless==4.5.3.56

# RUN pip install opencv-python-headless

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgl1 \
#     libglib2.0-0 \

# RUN apt-get update
# RUN apt install -y libgl1-mesa-glx

# RUN pip install opencv-contrib-python
# RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

# Update package lists and install necessary libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    ffmpeg \
    libfontconfig1 \
    libxrender1
# Install OpenCV with extra modules via pip
RUN pip install opencv-contrib-python

# Install the working directory          
WORKDIR /app


# Copy the files required to install dependencies
COPY poetry.lock pyproject.toml ./
# COPY poetry.lock $APP_HOME/poetry.lock
# COPY pyproject.toml $APP_HOME/pyproject.toml

# Set Poetry and dependences
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root
# RUN pip install poetry
# RUN poetry config virtualenvs.create false && poetry install --no-root


# Copy the rest of the project files
COPY . .


# Open port 8000
EXPOSE 8000

# Command start server
CMD ["sh", "-c", "python app_parking/manage.py runserver 0.0.0.0:8000"]

# & celery -A app_parking/manage.py beat -l info & celery -A app_parking/manage.py worker -l info -P eventlet
