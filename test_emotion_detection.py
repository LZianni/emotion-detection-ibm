"""Unit tests for Watson emotion detection and its Flask endpoint."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector
from server import app


class EmotionDetectionTests(unittest.TestCase):
    """Validate all five emotions, invalid input, and HTTP behavior."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_five_emotions(self, post):
        """Every supported emotion can be selected as dominant."""
        for emotion in ("joy", "anger", "disgust", "sadness", "fear"):
            with self.subTest(emotion=emotion):
                scores = dict.fromkeys(("anger", "disgust", "fear", "joy", "sadness"), 0.01)
                scores[emotion] = 0.96
                post.return_value = Mock(
                    status_code=200,
                    json=Mock(return_value={"emotionPredictions": [{"emotion": scores}]}),
                )
                result = emotion_detector(f"Example of {emotion}")
                self.assertEqual(result["dominant_emotion"], emotion)
                self.assertEqual(set(result), set(scores) | {"dominant_emotion"})

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, post):
        """The Watson API's HTTP 400 response returns empty scores."""
        post.return_value.status_code = 400
        self.assertTrue(all(value is None for value in emotion_detector("invalid").values()))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input(self, post):
        """Whitespace is rejected without contacting Watson."""
        self.assertIsNone(emotion_detector("  ")["dominant_emotion"])
        post.assert_not_called()

    def test_flask_blank_input(self):
        """The Flask route displays the expected error message."""
        with app.test_client() as client:
            response = client.get("/emotionDetector?textToAnalyze=")
            self.assertEqual(response.status_code, 400)
            self.assertIn(b"Invalid text! Please try again!", response.data)

    @patch("server.emotion_detector")
    def test_flask_success(self, detector):
        """The Flask route formats the detected emotion."""
        detector.return_value = {
            "anger": 0.01, "disgust": 0.01, "fear": 0.01,
            "joy": 0.96, "sadness": 0.01, "dominant_emotion": "joy",
        }
        with app.test_client() as client:
            response = client.get("/emotionDetector?textToAnalyze=happy")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"dominant emotion is joy", response.data)


if __name__ == "__main__":
    unittest.main()
