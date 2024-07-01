@echo off

echo Running App Update...
git init
git remote add origin https://github.com/daxcay/ImageDuplicateFinder.git

echo Running git pull...
git pull

:: Check if the virtual environment folder exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
    if ERRORLEVEL 1 (
        echo Failed to create virtual environment. Exiting.
        exit /b 1
    )
)

:: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if ERRORLEVEL 1 (
    echo Failed to activate virtual environment. Exiting.
    exit /b 1
)

:: Install required packages
echo Installing dependencies...
pip install -r requirements.txt
if ERRORLEVEL 1 (
    echo Failed to install dependencies. Exiting.
    exit /b 1
)

:: Run the Flask application
echo Running Flask application...
python app.py
if ERRORLEVEL 1 (
    echo Failed to run Flask application. Exiting.
    exit /b 1
)

:: Deactivate the virtual environment (optional)
echo Deactivating virtual environment...
deactivate

echo Application finished successfully.
