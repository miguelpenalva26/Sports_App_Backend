# Sports App — Backend
Dissertation project  
Miguel Penalva Caro

## Description
Django REST Framework backend - lightweight sports facility booking system. Handles booking validation, double booking prevention, user authentication and weather-based recommendations via OpenWeatherMap API.

## Characteristiics
- Backend validation to prevent double bookings
- Partial overlap and invalid time range detection
- Weather-based indoor/outdoor recommendations (OpenWeatherMap API)
- JWT user authentication
- RESTful API endpoints

## Requirements
- Python 3.x
- pip

## How to run
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## Frontend
The frontend is available at:  
https://github.com/miguelpenalva26/Sports_App

## Demo video
https://youtu.be/-RwF30kPmBk
