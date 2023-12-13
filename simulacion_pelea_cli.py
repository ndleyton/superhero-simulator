import requests
import random
import math
import typing
import time
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env
# To store the API key safely, but you can hardcode the API key here
API_KEY : int = os.getenv('MY_API_KEY') 
# number of possible superheroes in API
MAX_SUPERHEROES = 732
# Adjust number to adjust max of FB (Filiation Coefficient) and thus variance
MAX_FB = 9

# OOP superhero
class Superhero:
    def __init__(self, name, intelligence, strength, speed, durability, power, combat, alignment, image=''):
        # set the setting or random dependant attributes
        self.team_alignment = None
        self.fb = None
        self.actual_stamina = random.randint(0,9)
        self.fb_random = random.randint(0, MAX_FB)
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
    
    # Recalculate all stats taking into account AS and FB
    def adjust_all_stats(self) -> None:
        print ("pre adjustment:")
        print(self.__dict__)
        self.intelligence = self.adjusted_stat(self.intelligence)
        self.strength = self.adjusted_stat(self.strength)
        self.speed = self.adjusted_stat(self.speed)
        self.durability = self.adjusted_stat(self.durability)
        self.power = self.adjusted_stat(self.power)
        self.combat = self.adjusted_stat(self.combat)
        self.adjust_stat_hp()
        print("post adjustment:")
        print(self.__dict__)
    
    def adjust_stat_hp(self) -> None:
        """ Recalculate due to recalculating all stats"""
        self.hp = math.floor((self.strength * 0.8 + self.durability * 0.7 + self.power) / 2 * (1 + self.actual_stamina/ 10)) + 100  
        self.full_hp = self.hp
    
    def set_team_alignment(self, team_alignment) -> None:
        self.team_alignment = team_alignment
        self.set_fb(team_alignment=team_alignment)
        self.adjust_all_stats()
    
    def set_fb(self,team_alignment) -> None:
        if team_alignment == self.alignment:
            self.fb = 1 + self.fb_random
        else:
            self.fb = (1+self.fb_random) ** -1

    def random_attack(self) -> (str, int):
        """Choose a random attack and return its damage and type"""
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


    def take_damage(self, damage) -> int:
        """Receive damage, adjust hp and return resulting hp"""
        self.hp = max(self.hp - damage,0)
        return self.hp
    
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
        """ Now that we know the team affiliation, we can set the FB (Filiation Coefficient)"""
        for hero in self.alive_team:
            hero.set_team_alignment(self.team_alignment)

    def next_member(self) -> typing.Optional[Superhero]:
        if len(self.alive_team) > 0:
            return self.alive_team[0]
        return None

    def bury_member(self)->None:
        """Move a dead member from alive to dead list"""
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
    numbers = random.sample(range(733), n)
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
def simulate_fight(team1: Team, team2: Team):

    print("Battle Begins!")
    print("Team 1:",team1)
    print("Team 2:",team2)

    t1_fighter = team1.next_member()
    t2_fighter = team2.next_member()
    attack_order = [(team1,team2), (team2,team1)]

    # Simulate until one team is fully defeated
    while team1.next_member() and team2.next_member():
        # we randomize who attacks between the current fighters
        random_choice = random.randint(0,1)
        attacker_team, defender_team = attack_order[random_choice]
        attacker,defender = attacker_team.next_member(), defender_team.next_member()
        # attack only if both are alive
        if attacker.hp > 0 and defender.hp > 0:
            # Simple attack calculation: 10% of attacker's power is inflicted as damage
            attack_type, damage = attacker.random_attack()
            defender_hp = defender.take_damage(damage)
            print(f"{attacker.name} uses {attack_type} attack!  {defender.name} took {damage} damage. {defender.name} HP: {defender_hp}")
            # if attack killed
            if defender_hp <= 0:
                print(f"{defender.name} has died. ",end='')
                next_member_str = ""
                if random_choice == 0:
                    team2.bury_member()
                    t2_fighter = team2.next_member()
                    defender = t2_fighter
                    if t2_fighter:
                        next_member_str = f"{t2_fighter.name} steps in!"
                else:
                    team1.bury_member()
                    t1_fighter = team1.next_member()
                    defender = t1_fighter
                    if t1_fighter:
                        next_member_str = f"{t1_fighter.name} steps in!"
                print(next_member_str)     
            time.sleep(1)

    # Determine the winning team
    winner = "Team 1" if any(hero.hp > 0 for hero in team1.alive_team) else "Team 2"
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
    simulate_fight(team1, team2)
else:
    print("Failed to fetch superhero data.")



    

