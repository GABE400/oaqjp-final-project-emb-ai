from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_endpoint():
    """
    Endpoint to analyze emotions from the provided text.

    Returns:
        JSON response containing emotion scores and the dominant emotion,
        or an error message if the input is invalid.
    """
    data = request.get_json()
    text_to_analyze = data.get('textToAnalyze', '')

    # Call the emotion detector function
    result = emotion_detector(text_to_analyze)

    if result['dominant_emotion'] is None:
        return jsonify({"message": "Invalid text! Please try again!"}), 400

    # Format the response message
    response_message = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)