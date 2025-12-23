import requests

def generate_predictions(predict_url, ti):
    data = ti.xcom_pull(task_ids="clean_data")
    
    payload = {
        "texts": [item['text'] for item in data]
    }

    try:
        predict_response = requests.post(predict_url, json=payload)
    except:
        return
    
    if (predict_response.status_code != 200):
        return

    predictions = (predict_response.json())['predictions']

    return predictions