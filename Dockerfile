# Use the official Python image
FROM python:3.11
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
# Set the working directory inside the container
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


