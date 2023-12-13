import aiohttp
import asyncio
import random
import requests
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
def fetch_random_superheroes(api_key:str , max_superheroes:int=733, n=10) -> Optional[list]:
    #url = "https://akabab.github.io/superhero-api/api/all.json"
    numbers = random.sample(range(max_superheroes), n)
    superheroes = []
    for number in numbers:
        url = f"https://superheroapi.com/api/{api_key}/{number}"
        response = requests.get(url)
        if response.status_code == 200:
            hero = response.json()
            if hero['powerstats']['intelligence'] == 'null':
                hero['powerstats']['intelligence'] = 0
            if hero['powerstats']['strength'] == 'null':
                hero['powerstats']['strength'] = 0
            if hero['powerstats']['speed'] == 'null':
                hero['powerstats']['speed'] = 0
            if hero['powerstats']['durability'] == 'null':
                hero['powerstats']['durability'] = 0
            if hero['powerstats']['power'] == 'null':
                hero['powerstats']['power'] = 0
            if hero['powerstats']['combat'] == 'null':
                hero['powerstats']['combat'] = 0

            superheroes.append(hero)
    return superheroes

# Async versions since fetch_random_superheroes is doing 10 consecutive http reuqests

async def fetch_hero(session, url):
    async with session.get(url) as response:
        return await response.json()

async def async_fetch_random_superheroes(api_key: str, max_superheroes:int=733, n=10):
    numbers = random.sample(range(max_superheroes), n)
    superheroes = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for number in numbers:
            url = f"https://superheroapi.com/api/{api_key}/{number}"
            tasks.append(asyncio.ensure_future(fetch_hero(session, url)))

        responses = await asyncio.gather(*tasks)

        for hero in responses:
            if hero['powerstats']['intelligence'] == 'null':
                hero['powerstats']['intelligence'] = 0
                if hero['powerstats']['strength'] == 'null':
                    hero['powerstats']['strength'] = 0
                if hero['powerstats']['speed'] == 'null':
                    hero['powerstats']['speed'] = 0
                if hero['powerstats']['durability'] == 'null':
                    hero['powerstats']['durability'] = 0
                if hero['powerstats']['power'] == 'null':
                    hero['powerstats']['power'] = 0
                if hero['powerstats']['combat'] == 'null':
                    hero['powerstats']['combat'] = 0

            superheroes.append(hero)
    return superheroes