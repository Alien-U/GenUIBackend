#!/bin/bash
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Running Database Migrations..."
python3.9 manage.py migrate --noinput