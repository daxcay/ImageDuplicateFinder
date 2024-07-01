#!/bin/bash

echo "Running App Update..."
git init
git remote add origin https://github.com/daxcay/ImageDuplicateFinder.git

echo "Running git pull..."
git pull

# Check if the virtual environment folder exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Exiting."
        exit 1
    fi
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Exiting."
    exit 1
fi

# Install required packages
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Exiting."
    exit 1
fi

# Run the Flask application
echo "Running Flask application..."
python3 app.py
if [ $? -ne 0 ]; then
    echo "Failed to run Flask application. Exiting."
    exit 1
fi

# Deactivate the virtual environment (optional)
echo "Deactivating virtual environment..."
deactivate

echo "Application finished successfully."
