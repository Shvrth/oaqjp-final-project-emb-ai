# final_project/emotion_detection.py
import requests
import argparse
import json

def emotion_detector(text_to_analyze):
    # Define API configuration FIRST
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}
    
    # Then declare result template
    result = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # Correct response parsing
        emotions = data.get('emotionPredictions', {})[0].get('emotion', {})
        # Update results
        result.update({
            'anger': emotions.get('anger'),
            'disgust': emotions.get('disgust'),
            'fear': emotions.get('fear'),
            'joy': emotions.get('joy'),
            'sadness': emotions.get('sadness')
        })

        # Find dominant emotion
        if any(result.values()):
            emotions_only = {k: v for k, v in result.items() if k != 'dominant_emotion'}
            result['dominant_emotion'] = max(emotions_only.items(), key=lambda x: x[1])[0]

    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze text emotion')
    parser.add_argument('--text', type=str, required=True, help='Text to analyze')
    args = parser.parse_args()
    
    analysis = emotion_detector(args.text)
    print(json.dumps(analysis, indent=2))