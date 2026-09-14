"""
Train the Sarada Residential flat price model.

Usage:
    python train_model.py [--data path/to/dataset.csv]

Expects a CSV with columns:
    Area_Sqft, Floor, Car_Parking_Sqft, Bedrooms, Edit_face, Price

Edit_face is the facing encoded as: East=1, West=2, North=3, South=4.
Writes api/model.pkl (the file the app and serverless function load).
"""

import argparse

import pandas as pd

from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
)

from sklearn.model_selection import train_test_split

FEATURES = [
    "Area_Sqft",
    "Floor",
    "Car_Parking_Sqft",
    "Bedrooms",
    "Edit_face",
]

TARGET = "Price"

MODEL_PATH = "api/model.pkl"

FACING_MAP = {"East": 1, "West": 2, "North": 3, "South": 4}


def main():
    parser = argparse.ArgumentParser(
        description="Train the flat price model"
    )
    parser.add_argument(
        "--data",
        default="data/dataset.csv",
        help="Path to the training CSV",
    )
    args = parser.parse_args()

    data = pd.read_csv(args.data)

    missing = [
        column
        for column in FEATURES + [TARGET]
        if column not in data.columns
    ]

    if missing:
        raise SystemExit(
            f"Dataset is missing columns: {missing}"
        )

    if "Facing" in data.columns and "Edit_face" not in data.columns:
        data["Edit_face"] = data["Facing"].map(FACING_MAP)

    data = data.dropna(
        subset=FEATURES + [TARGET]
    )

    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("MAE    :", mean_absolute_error(y_test, predictions))
    print("R2     :", r2_score(y_test, predictions))
    print("Features:", FEATURES)

    import os
    import pickle

    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True,
    )

    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)

    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
