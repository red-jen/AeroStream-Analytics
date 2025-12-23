import requests

def fetch_data(url, size):
    
    params = {"batch_size": size}

    try:
        response = requests.get(url, params=params)
    except:
        print("Error! Could not fetch data from the API")
        return []
    
    if response.status_code != 200:
        print("Error! Could not fetch data from the API")
        return []

    data = response.json()

    print("data was loaded successfully !")
    return data