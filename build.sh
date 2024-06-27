#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Ensure pip is installed
echo "Ensuring pip is installed..."
python3.9 -m ensurepip --upgrade

# Upgrade pip
echo "Upgrading pip..."
python3.9 -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
python3.9 -m pip install -r requirements.txt

# Apply database migrations
echo "Making Migrations..."
python3.9 manage.py makemigrations --noinput

echo "Applying Migrations..."
python3.9 manage.py migrate --noinput

# Collect static files
echo "Collecting Static Files..."
python3.9 manage.py collectstatic --noinput --clear