# Emotion Detection Web Application

Final project for the IBM course **Developing AI Applications with Python and Flask**.

This Flask application sends English text to the IBM Skills Network Watson NLP EmotionPredict endpoint and returns anger, disgust, fear, joy, sadness, and the dominant emotion.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m unittest -v test_emotion_detection.py
python3 -m pylint server.py EmotionDetection
python3 server.py
```

Open http://localhost:5000 and enter `I think I am having fun`.

**Important:** The IBM Skills Network endpoint may only be reachable from the course lab. The unit tests use mocks so they run without network access; real predictions require access to the IBM service.

## API

`GET /emotionDetector?textToAnalyze=I%20think%20I%20am%20having%20fun`

Blank input returns HTTP 400 and `Invalid text! Please try again!`.

## Submission checklist

1. Publish this repository to your own public GitHub account. Submit the link to `README.md`.
2. Submit `EmotionDetection/emotion_detection.py` and a terminal screenshot of a successful real Watson prediction.
3. Submit the formatted function and its real prediction output.
4. Submit the link to `EmotionDetection/__init__.py` and the package import evidence.
5. Submit `test_emotion_detection.py` and the real passing unit-test output.
6. Submit `server.py` and capture the running browser as `6b_deployment_test.png`.
7. Submit the updated source files and capture a blank-text response as `7c_error_handling_interface.png`.
8. Submit `server.py` and the real Pylint output. A perfect score must be verified in your environment.

## Notes

- Do not present mocked tests as proof of a real Watson API call.
- The development Flask server is not a production deployment.
