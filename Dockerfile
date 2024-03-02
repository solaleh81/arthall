# Use the official Python image as the base image
FROM python:3.11.6

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    virtualenv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install dependencies
RUN python -m venv venv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Command to run the application
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
