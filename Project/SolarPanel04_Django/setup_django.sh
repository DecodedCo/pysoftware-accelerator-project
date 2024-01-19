#!/bin/bash

cd src && mkdir solar_project && cd solar_project
django-admin startproject solar_project . 
django-admin startapp solar_web 
django-admin startapp solar_api

echo "INSTALLED_APPS += ['solar_web', 'solar_api', 'rest_framework']" >> solar_project/settings.py

mkdir solar_web/static

home_html=$(cat ref/home.html)
result_html=$(cat ref/result.html)

echo "$home_html" > solar_web/static/home.html
echo "$result_html" > solar_web/static/result.html
