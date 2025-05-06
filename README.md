# Weather Info & Forecast Bot using Google Dialogflow ES

## Overview
This project is a state-of-the-art chatbot that provides current weather information and 5-day forecasts for any city, using Google Dialogflow ES for natural language understanding and a FastAPI backend for weather data retrieval via the OpenWeatherMap API.

## Features
- Get current weather for any city
- Get weather forecast for up to 5 days ahead
- Natural language conversation powered by Dialogflow ES
- Robust error handling for unknown cities and API issues
- Easily extensible and well-documented codebase

## Tech Stack
- **Backend:** Python, FastAPI, httpx
- **Chatbot:** Google Dialogflow ES
- **Weather Data:** OpenWeatherMap API
- **Tunnel:** ngrok (for local development)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd weather_bot/api
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv venv
./venv/Scripts/activate  # On Windows
# Or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the `api` directory with the following content:
```
Open_Weather_Map_Api_Key=YOUR_OPENWEATHERMAP_API_KEY
```
Replace `YOUR_OPENWEATHERMAP_API_KEY` with your actual API key from [OpenWeatherMap](https://openweathermap.org/api).

### 5. Run the FastAPI Server
```sh
python -m uvicorn app:app --reload
```

### 6. Expose Your Local Server with ngrok
Download ngrok from [ngrok.com](https://ngrok.com/download) and run:
```sh
grok http 8000
```
Copy the HTTPS forwarding URL (e.g., `https://xxxx.ngrok-free.app`).

## Dialogflow Integration

### 1. Create a Dialogflow ES Agent
- Go to [Dialogflow ES Console](https://dialogflow.cloud.google.com/)
- Click "Create Agent" and fill in the details

### 2. Set Up Fulfillment
- Go to the **Fulfillment** tab
- Enable the webhook
- Enter your ngrok URL with `/webhook` at the end (e.g., `https://xxxx.ngrok-free.app/webhook`)
- Save

### 3. Create Intents
#### a. Get Current Weather Intent
- Add training phrases like "What's the weather in Paris?"
- Add a required parameter: `city` with entity `@sys.geo-city`
- Enable webhook call for this intent

#### b. Get Weather Forecast Intent
- Add training phrases like "What's the weather in Paris on Friday?"
- Add required parameters: `city` (`@sys.geo-city`), `date` (`@sys.date`)
- Enable webhook call for this intent

### 4. Test Your Agent
- Use the "Try it now" chat window in Dialogflow
- Example queries:
  - "What's the weather in New York?"
  - "Weather forecast for London on 2025-05-10"

## Error Handling
- If the city is not recognized, the bot will prompt for a valid city
- If the date is out of forecast range, the bot will return current weather
- Handles API/network errors gracefully

## Submission Guidelines
- Push your code to a public GitHub repository
- Export your Dialogflow agent (Settings → Export and Import → Export as ZIP)
- Record a demo video showing the bot in action and explaining your approach
- Email the Dialogflow agent ZIP and your GitHub repo link as instructed

## Example API Request
```sh
curl -X POST "http://127.0.0.1:8000/webhook" -H "Content-Type: application/json" -d '{"city": "Paris"}'
```

## License
This project is for evaluation and educational purposes.
