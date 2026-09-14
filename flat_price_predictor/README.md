# Sarada Residential — Flat Price Predictor

A premium flat-price estimation site for **Sarada Residential**: an animated
night-city frontend, a validated prediction API, and a one-command deploy to
**Vercel** (static frontend + Python serverless function).

```
flat_price_predictor/
├── public/            ← static frontend (served as-is)
│   ├── index.html     ← the whole UI
│   └── static/
│       └── styles.css
├── api/               ← serverless backend
│   ├── model.pkl      ← trained LinearRegression model
│   ├── common.py      ← model loading, validation, prediction
│   └── predict.py     ← Vercel function (POST /api/predict)
├── app.py             ← local Flask wrapper (same routes as Vercel)
├── train_model.py     ← retrains api/model.pkl from a dataset CSV
├── vercel.json        ← routing: / → frontend, /predict → function
├── .vercelignore
└── requirements.txt
```

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (source .venv/bin/activate on mac/linux)
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

- `GET  /`        → the site (served from `public/`)
- `POST /predict` → form data or JSON: `area, facing, floor, bedrooms, car_parking`
- `GET  /health`  → `{"status": "ok", "model_loaded": true}`

## Deploy to Vercel

```bash
npm i -g vercel
vercel          # preview deploy
vercel --prod   # production
```

`vercel.json` routes `/` (and any non-API path) to `public/index.html` and
`/predict` → `api/predict.py`, so the frontend code works unchanged on
Vercel and locally. No environment variables are required.

## Retrain the model

```bash
python train_model.py --data data/dataset.csv
```

The CSV needs columns `Area_Sqft, Floor, Car_Parking_Sqft, Bedrooms,
Edit_face, Price` (`Edit_face`: East=1, West=2, North=3, South=4).
This writes `api/model.pkl`, which both the local app and the serverless
function load. The model is trained with **scikit-learn 1.6.1** — keep that
pin in `requirements.txt` when retraining to avoid version-mismatch warnings.
