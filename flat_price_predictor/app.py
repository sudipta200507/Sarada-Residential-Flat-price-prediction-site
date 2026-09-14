import os

from http import HTTPStatus

from flask import Flask, jsonify, request

from api.common import (
    InvalidInput,
    load_model,
    run_prediction,
)

_static_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "public",
)

app = Flask(
    __name__,
    static_folder=_static_dir,
    static_url_path="",
)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": load_model() is not None,
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        price = run_prediction(
            request.form.to_dict()
        )
        return jsonify({"prediction": price})

    except InvalidInput as error:
        return jsonify({
            "error": "Validation failed",
            "details": str(error),
        }), HTTPStatus.BAD_REQUEST

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed",
        }), HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
