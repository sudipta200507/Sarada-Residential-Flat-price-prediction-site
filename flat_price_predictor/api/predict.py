import json

from urllib.parse import parse_qs

from werkzeug.wrappers import Response

from api.common import InvalidInput, run_prediction

_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def handler(request):
    """
    Vercel Python serverless function.
    Deployed as POST /api/predict.
    """
    if request.method == "OPTIONS":
        return _response(204, {})

    if request.method != "POST":
        return _response(405, {
            "error": "Method not allowed. Use POST."
        })

    try:
        payload = _extract_payload(request)
        price = run_prediction(payload)
        return _response(200, {"prediction": price})

    except InvalidInput as error:
        return _response(400, {
            "error": "Validation failed",
            "details": str(error),
        })

    except Exception:
        return _response(500, {
            "error": "Prediction failed"
        })


def _extract_payload(request):
    """
    Vercel's Python runtime passes the raw body as a
    string/bytes on `request.body`, so parse JSON first
    and fall back to form-encoded data.
    """
    body = getattr(request, "body", None)

    if isinstance(body, (bytes, str)) and body:
        text = (
            body.decode("utf-8")
            if isinstance(body, bytes)
            else body
        )

        try:
            return json.loads(text)

        except (json.JSONDecodeError, ValueError):
            parsed = parse_qs(
                text,
                keep_blank_values=True,
            )
            return {
                key: values[0]
                for key, values in parsed.items()
            }

    form = getattr(request, "form", None)
    if form:
        return form.to_dict()

    return {}


def _response(status, data):
    return Response(
        json.dumps(data) if data else "",
        status=status,
        headers=_CORS_HEADERS,
    )
