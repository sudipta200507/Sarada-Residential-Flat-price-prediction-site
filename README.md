# Sarada Residential — Flat Price Predictor

A premium flat-price estimation site for **Sarada Residential**: an animated
night-city frontend, a validated prediction API, and a **zero-config deploy
to Vercel** (Flask app + static frontend in one project).

```
flat_price_predictor/
├── public/            ← static frontend (served by Flask AND Vercel)
│   ├── index.html     ← the whole UI
│   └── static/
│       └── styles.css
├── app.py             ← Flask entrypoint (Vercel loads `app` from here)
├── predictor.py       ← model loading, validation, prediction
├── model.pkl          ← trained LinearRegression model
├── train_model.py     ← retrains model.pkl from a dataset CSV
├── requirements.txt   ← Flask, numpy, pandas, scikit-learn (pinned)
└── .vercelignore
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
- `POST /predict` → form data **or** JSON: `area, facing, floor, bedrooms, car_parking`
- `GET  /health`  → `{"status": "ok", "model_loaded": true}`

## Deploy to Vercel

No `vercel.json` needed. Vercel detects Flask from `requirements.txt`,
loads the `app` variable from `app.py`, routes every request to it, and
serves `public/` automatically — the same app you run locally deploys as-is.

Push this repo to GitHub, then either:

- **Dashboard:** vercel.com → *Add New Project* → import the repo → Deploy
- **CLI:** `npm i -g vercel && vercel --prod`

No environment variables are required.

## Retrain the model

```bash
python train_model.py --data data/dataset.csv
```

The CSV needs columns `Area_Sqft, Floor, Car_Parking_Sqft, Bedrooms,
Edit_face, Price` (`Edit_face`: East=1, West=2, North=3, South=4).
This writes `model.pkl`, which the app loads. The model is trained with
**scikit-learn 1.6.1** — keep that pin in `requirements.txt` when
retraining to avoid version-mismatch warnings.
