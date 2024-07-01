# pull official base image
FROM python:3.10.14-slim-bullseye

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY .. /app