# Use the official image of Python
FROM python:3.11


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
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
