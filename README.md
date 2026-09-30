# Sarada Residential — Flat Price Predictor

A production-style web application for estimating residential flat prices using a trained machine-learning model exposed through a Flask API.

## Overview

This project turns a regression model into a usable web application:

`text
User Input
   ↓
Frontend
   ↓
Flask API
   ↓
Input Validation
   ↓
ML Model
   ↓
Predicted Price
`

The project demonstrates the transition from ML experimentation to deployable software.

## Features

- Interactive flat-price estimation UI
- Flask prediction API
- Input validation
- Trained scikit-learn regression model
- Health endpoint
- Vercel deployment support
- Local development workflow
- Model retraining script

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML / CSS / JavaScript |
| Backend | Flask |
| ML | scikit-learn |
| Data | Pandas / NumPy |
| Deployment | Vercel |
| Language | Python |

## Project Structure

`text
flat_price_predictor/
├── public/
│   ├── index.html
│   └── static/
│       └── styles.css
├── app.py
├── predictor.py
├── model.pkl
├── train_model.py
├── requirements.txt
└── .vercelignore
`

## Run Locally

`bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
`

Open `http://127.0.0.1:5000`.

### API

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Web application |
| `/predict` | POST | Generate a price prediction |
| `/health` | GET | Service health check |

## Retrain the Model

`bash
python train_model.py --data data/dataset.csv
`

Expected dataset fields include:

`text
Area_Sqft
Floor
Car_Parking_Sqft
Bedrooms
Edit_face
Price
`

## Deployment

The application is structured for deployment on Vercel using the Flask entrypoint in `app.py`.

## Engineering Focus

- Serving ML models through APIs
- Input validation
- Model serialization
- Frontend/backend integration
- Deployment-oriented project structure
- Reproducible model retraining

## Author

**Sudipta Roy**  
B.Tech CSE (AI & ML)
