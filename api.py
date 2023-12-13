import requests
import random
from typing import List, Optional


# Function to fetch all superhero data from the API
def fetch_all_superheroes() -> Optional[dict]:
    url = "https://akabab.github.io/superhero-api/api/all.json"
    #url = f"https://superheroapi.com/api/{API_KEY}/all.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function to fetch superhero data from the API
def fetch_random_superheroes(api_key:str , n=10) -> Optional[dict]:
    #url = "https://akabab.github.io/superhero-api/api/all.json"
    numbers = random.sample(range(733), n)
    url = f"https://superheroapi.com/api/{api_key}/all.json"
    response = requests.get(url)
    # print(f"response: {response}")
    if response.status_code == 200:
        return response.json()
    else:
        return None