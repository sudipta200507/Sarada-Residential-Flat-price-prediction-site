import logging
import os
import pickle

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("sarada")

FEATURE_NAMES = [
    "Area_Sqft",
    "Floor",
    "Car_Parking_Sqft",
    "Bedrooms",
    "Edit_face",
]

FACING_MAP = {
    "East": 1,
    "West": 2,
    "North": 3,
    "South": 4,
}

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "model.pkl",
)

model = None


def load_model():
    """Load model.pkl once per process."""
    global model
    if model is not None:
        return model
    try:
        with open(MODEL_PATH, "rb") as file:
            model = pickle.load(file)
        log.info("Model loaded from %s", MODEL_PATH)
    except Exception:
        log.exception("Failed to load model")
        model = None
    return model


class InvalidInput(ValueError):
    """Raised when user input fails validation."""


def _to_float(value, field, minimum, maximum):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise InvalidInput(f"{field} must be a number")

    if not np.isfinite(number):
        raise InvalidInput(f"{field} must be finite")

    if number < minimum or number > maximum:
        raise InvalidInput(
            f"{field} must be between "
            f"{minimum:g} and {maximum:g}"
        )

    return number


def parse_payload(payload):
    """
    Accept form-encoded or JSON payloads and return a
    validated one-row DataFrame with the training
    feature names.
    """
    if not isinstance(payload, dict):
        raise InvalidInput("Invalid payload")

    def get(key):
        value = payload.get(key)
        if isinstance(value, list):
            return value[0] if value else None
        return value

    area = _to_float(get("area"), "Area", 10, 100000)
    facing = get("facing")
    floor = _to_float(get("floor"), "Floor", 0, 200)
    bedrooms = _to_float(get("bedrooms"), "Bedrooms", 1, 20)
    parking = _to_float(get("car_parking"), "Car parking", 0, 10000)

    if facing not in FACING_MAP:
        raise InvalidInput(
            "Facing must be one of: " +
            ", ".join(FACING_MAP)
        )

    row = {
        "Area_Sqft": area,
        "Floor": floor,
        "Car_Parking_Sqft": parking,
        "Bedrooms": bedrooms,
        "Edit_face": FACING_MAP[facing],
    }

    return pd.DataFrame(
        [row],
        columns=FEATURE_NAMES,
    )


def run_prediction(payload):
    """
    Validate the payload and return the predicted
    price in lakhs as a float.
    """
    current = load_model()
    if current is None:
        raise RuntimeError("Model failed to load")

    frame = parse_payload(payload)
    prediction = current.predict(frame)
    return float(prediction[0])
