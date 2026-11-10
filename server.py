"""Flask interface for the Watson NLP emotion detector."""

from flask import Flask, render_template, request
from requests import RequestException

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Display the emotion detection interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze the text supplied by the browser."""
    text = request.args.get("textToAnalyze", "")
    if not text.strip():
        return "Invalid text! Please try again!", 400

    try:
        result = emotion_detector(text)
    except (RequestException, KeyError, IndexError, ValueError):
        app.logger.exception("Emotion detection service failed")
        return "Emotion detection service unavailable. Please try again later.", 503

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    scores = ", ".join(
        f"'{emotion}': {result[emotion]}"
        for emotion in ("anger", "disgust", "fear", "joy", "sadness")
    )
    return (
        f"For the given statement, the system response is {scores}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
