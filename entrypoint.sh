#!/bin/bash

echo "Starting the application..."
python manage.py makemigrations
python manage.py migrate
python manage.py populate & # --file starlink.json

echo "Application has been started..."