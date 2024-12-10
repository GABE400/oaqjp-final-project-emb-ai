import requests
import json
import time

def emotion_detector(text_to_analyze, max_retries=3, timeout=10):
    if not text_to_analyze.strip():  # Check for blank input
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=input_json, timeout=timeout)

            if response.status_code == 200:
                response_data = response.json()
                
                anger_score = response_data.get('emotion', {}).get('anger', 0)
                disgust_score = response_data.get('emotion', {}).get('disgust', 0)
                fear_score = response_data.get('emotion', {}).get('fear', 0)
                joy_score = response_data.get('emotion', {}).get('joy', 0)
                sadness_score = response_data.get('emotion', {}).get('sadness', 0)

                emotions_dict = {
                    'anger': anger_score,
                    'disgust': disgust_score,
                    'fear': fear_score,
                    'joy': joy_score,
                    'sadness': sadness_score
                }

                dominant_emotion = max(emotions_dict, key=emotions_dict.get)
                emotions_dict['dominant_emotion'] = dominant_emotion

                return emotions_dict
            
            elif response.status_code == 400:  # Handle bad request for blank input
                return {
                    'anger': None,
                    'disgust': None,
                    'fear': None,
                    'joy': None,
                    'sadness': None,
                    'dominant_emotion': None
                }
        
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt + 1} timed out. Retrying...")
            time.sleep(2)  
        except requests.exceptions.ConnectionError:
            return "Error: Connection failed. Please check your internet connection."
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    return "Error: Maximum retry attempts exceeded."