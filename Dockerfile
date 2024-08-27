# Use the official image of Python
FROM python:3.8

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

# # Update package lists and install necessary libraries
# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     libsm6 \
#     libxext6 \
#     ffmpeg \
#     libfontconfig1 \
#     libxrender1
# # Install OpenCV with extra modules via pip
# RUN pip install opencv-contrib-python

# # Update package lists and install necessary libraries
# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     libsm6 \
#     libxext6 \
#     ffmpeg \
#     libfontconfig1 \
#     libxrender1
# # Install OpenCV with extra modules via pip
# RUN pip install opencv-python paddlepaddle paddleocr


# Update package lists and install necessary libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    ffmpeg \
    libfontconfig1 \
    libxrender1
# Install a specific version of PaddlePaddle
RUN pip install paddlepaddle==2.5.1 paddleocr opencv-python
# Disable CPU optimizations that may not be supported
ENV FLAGS_use_mkldnn=False
ENV FLAGS_use_mkldnn_quantizer=False

# Install the working directory          
WORKDIR /app
# Copy the files required to install dependencies
COPY poetry.lock pyproject.toml ./
# Set up Poetry and install project dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root
# Copy the rest of the project files into the container
COPY . .
# Expose port 8000 for the Django server
EXPOSE 8000
# Command to start the Django server
CMD ["sh", "-c", "python3 app_parking/manage.py makemigrations && python3 app_parking/manage.py migrate && python3 app_parking/manage.py runserver 0.0.0.0:8000"]

# & celery -A app_parking/manage.py beat -l info & celery -A app_parking/manage.py worker -l info -P eventlet
