import requests
import random
import math
import typing
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env
# To store the API key safely, but you can hardcode the API key here
API_KEY : int = os.getenv('MY_API_KEY') 

#number of possible superheroes in API
MAX_SUPERHEROES = 732

# OOP superhero
class Superhero:
    def __init__(self, name, intelligence, strength, speed, durability, power, combat, alignment, image=''):
        # set the setting or random dependant attributes
        self.team_alignment = None
        self.fb = None
        self.actual_stamina = random.randint(0,9)
        self.fb_random = random.randint(0,9)
        # set the API dependant attributes
        self.name = name
        self.intelligence = intelligence
        self.strength = strength
        self.speed = speed
        self.durability = durability
        self.power = power
        self.combat = combat
        self.alignment = alignment
        self.image = image
        self.hp = math.floor((strength * 0.8 + durability * 0.7 + power) / 2 * (1 + self.actual_stamina/ 10)) + 100  # Initial HP
        self.full_hp = self.hp
        

    def adjusted_stat(self, previous: int) -> int:
        # stats = math.floor(((2 * Base + AS) / 1.1) * FB)
        return math.floor(((2 * previous + self.actual_stamina) / 1.1) * self.fb)
    
    def set_team_alignment(self, team_alignment) -> None:
        self.team_alignment = team_alignment
        self.set_fb(team_alignment=team_alignment)
    
    def set_fb(self,team_alignment) -> None:
        if team_alignment == self.alignment:
            self.fb = 1 + self.fb_random
        else:
            self.fb = (1+self.fb_random) ** -1

    def random_attack(self) -> (str, int):
        chosen_index = random.randint(0,2)
        damage = 0
        attack_type = ""
        if chosen_index == 0:
            damage = (self.intelligence * 0.7 + self.speed * 0.2 + self.combat * 0.1) * self.fb
            attack_type = "Mental"
        elif chosen_index == 1:
            damage = (self.strength * 0.6 + self.power * 0.2 + self.combat * 0.2) * self.fb
            attack_type = "Strong"
        else:
            damage = (self.speed * 0.55 + self.durability * 0.25 + self.strength * 0.2) * self.fb
            attack_type = "Fast"
        return(attack_type, math.floor(damage))

    def mental_attack(self):
        damage = (self.intelligence * 0.7 + self.speed * 0.2 + self.combat * 0.1) * self.fb
    
    def strong_attack(self):
        damage = (self.strength * 0.6 + self.power * 0.2 + self.combat * 0.2) * self.fb
    
    def fast_attack(self):
        damage = (self.speed * 0.55 + self.durability * 0.25 + self.strength * 0.2) * self.fb
    
    def heal(self) -> None:
        self.hp = self.full_hp
    
    def is_alive(self) -> bool:
        return self.hp > 0

    def __str__(self) -> str:
        return f"{self.name} (HP: {self.hp})"

# Superhero team class
class Team:
    def __init__(self, heroes: list[Superhero]= []):
        self.alive_team = heroes
        self.dead_team = []
        self.good_members = 0
        self.total_members = len(self.alive_team)
        self.team_alignment = None
        if self.total_members > 0:
            self.set_team_alignment()
            self.set_members_filiation_coefficient()
    
    def set_team_alignment(self):
        good_members = 0
        for hero in self.alive_team:
            if hero.alignment == 'good':
                good_members += 1
        
        # majority of team is good
        if good_members > self.total_members//2:
            self.team_alignment = 'good'
        else:
            self.team_alignment = 'bad'
    
    def set_members_filiation_coefficient(self):
        # Now that we know the team affiliation, we can set the FB (Filiation Coefficient)
        for hero in self.alive_team:
            hero.set_team_alignment(self.team_alignment)

    def next_member(self) -> typing.Optional[Superhero]:
        if len(self.is_alive) > 0:
            return self.alive_team[0]
        return None

    def bury_member(self):
        # fighting member is always index 0
        self.dead_team.append( self.alive_team.pop(0))
    
    def __str__(self):
        alive = [hero.name for hero in self.alive_team]
        return " | ".join(alive)

# Function to fetch all superhero data from the API
def fetch_all_superheroes():
    url = "https://akabab.github.io/superhero-api/api/all.json"
    #url = f"https://superheroapi.com/api/{API_KEY}/all.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function to fetch superhero data from the API
def fetch_random_superheroes(n=10):
    #url = "https://akabab.github.io/superhero-api/api/all.json"

    url = f"https://superheroapi.com/api/{API_KEY}/all.json"
    response = requests.get(url)
    # print(f"response: {response}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Use the fetched superheroes to choose the needed ones and create classes for each
def populate_superheroes(heroes_data: dict = {}, n:int = 10,) -> list[Superhero]:
    # Convert the dictionary values to a list
    heroes_list = list(heroes_data)
    random_heroes = random.sample(heroes_list, n)

    superheroes = []
    for hero in random_heroes:
        superheroes.append(Superhero(
            hero['name'],
            hero['powerstats']['intelligence'],
            hero['powerstats']['strength'],
            hero['powerstats']['speed'],
            hero['powerstats']['durability'],
            hero['powerstats']['power'],
            hero['powerstats']['combat'],
            hero['biography']['alignment'],
            hero['images']['xs']
        ))
    # 'image''url' in superheroapi.com, but 'images''xs' in akabab.github.io/superhero-api
    return superheroes


# Simulate the fight
def simulate_fight(team1, team2):

    print("Battle Begins!")
    print("Team 1:", [hero.name for hero in team1])
    print("Team 2:", [hero.name for hero in team2])

    # Simulate until one team is fully defeated
    while any(hero.hp > 0 for hero in team1) and any(hero.hp > 0 for hero in team2):
        # Each team member attacks a random member of the opposing team
        for attacker, defender in zip(random.sample(team1, len(team1)), random.sample(team2, len(team2))):
            if attacker.hp > 0 and defender.hp > 0:
                # Simple attack calculation: 10% of attacker's power is inflicted as damage
                attack_type, damage = attacker.random_attack()
                defender.hp = max(defender.hp - damage, 0)
                print(f"{attacker.name} uses {attack_type} attack! {defender.name} causing {damage} damage. {defender.name} HP: {defender.hp}")

    # Determine the winning team
    winner = "Team 1" if any(hero.hp > 0 for hero in team1) else "Team 2"
    print("\nWinner:", winner)

# Fetch superheroes
superheroes = fetch_all_superheroes()
if superheroes:
    # Select 10 random superheroes and divide them into two teams
    selected_heroes = populate_superheroes(superheroes)
    team1_data, team2_data = selected_heroes[:5], selected_heroes[5:]
    # set up the team alignments
    team1, team2= Team(team1_data) ,Team(team2_data)

    # Simulate the fight
    simulate_fight(team1_data, team2_data)
else:
    print("Failed to fetch superhero data.")



    

