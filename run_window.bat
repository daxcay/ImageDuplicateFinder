@echo off

:: Check if the virtual environment folder exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install required packages
echo Installing dependencies...
pip install -r requirements.txt

:: Run the Flask application
echo Running Flask application...
python app.py

:: Deactivate the virtual environment (optional)
:: deactivate
