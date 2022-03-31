#!/bin/bash

echo "Starting the application..."
python manage.py makemigrations
python manage.py makemigrations api_space
python manage.py migrate
python manage.py migrate api_space
python manage.py runserver 0.0.0.0:8000

echo "Application has been started..."