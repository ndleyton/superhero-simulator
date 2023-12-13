import requests
import random
import math
import time
from itertools import zip_longest
from typing import List, Optional, Tuple
import os
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.text import Text
from rich.live import Live
from rich.layout import Layout

from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env

# To store the API key safely, but you can hardcode the API key here
API_KEY : Optional[str] = os.getenv('MY_API_KEY') 
# number of possible superheroes in API
MAX_SUPERHEROES = 732
# Adjust number to adjust max of FB (Filiation Coefficient) and thus variance
MAX_FB = 9
# Adjust to set the time spent between actions
SLEEP_TIME = 0.4


console = Console() # Console for TUI

# OOP superhero
class Superhero:
    """Class representing a Superhero with necessary attributes and methods to fight and keep track of health"""
    def __init__(self, name, intelligence, strength, speed, durability, power, combat, alignment, image=''):
        # set the setting or random dependant attributes
        self.team_alignment = None
        self.fb = None
        self.actual_stamina : int = random.randint(0,9)
        self.fb_random : int = random.randint(0, MAX_FB)
        # set the API dependant attributes
        self.name : str = name
        self.intelligence : int = intelligence
        self.strength: int = strength
        self.speed : int  = speed
        self.durability : int = durability
        self.power : int = power
        self.combat : int = combat
        self.alignment : str = alignment
        self.image = image
        self.hp = math.floor((strength * 0.8 + durability * 0.7 + power) / 2 * (1 + self.actual_stamina/ 10)) + 100  # Initial HP
        self.full_hp = self.hp
    

    def adjusted_stat(self, previous: int) -> int:
        # stats = math.floor(((2 * Base + AS) / 1.1) * FB)
        return math.floor(((2 * previous + self.actual_stamina) / 1.1) * self.fb)
    
    # Recalculate all stats taking into account AS and FB
    def adjust_all_stats(self) -> None:
        self.intelligence = self.adjusted_stat(self.intelligence)
        self.strength = self.adjusted_stat(self.strength)
        self.speed = self.adjusted_stat(self.speed)
        self.durability = self.adjusted_stat(self.durability)
        self.power = self.adjusted_stat(self.power)
        self.combat = self.adjusted_stat(self.combat)
        self.adjust_stat_hp()
    
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

    def random_attack(self) -> Tuple[str, int]:
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
        return f"{self.name}    HP: {self.hp}/{self.full_hp})"

# Superhero team class
class Team:
    """Class representing a team of Superheroes."""
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

    def next_member(self) -> Optional[Superhero]:
        if len(self.alive_team) > 0:
            return self.alive_team[0]
        return None
    
    def member_idx(self, idx:int)->Text:
        output = Text("")
        if idx < self.total_members:
            members = self.alive_team + self.dead_team
            hero = members[idx]
            output = Text(f"{hero.name}    HP:{hero.hp}/{hero.full_hp}", style="green" if hero.hp > 0 else "red strike")
        return output

    def bury_member(self)->None:
        """Move a dead member from alive to dead list"""
        # fighting member is always index 0
        self.dead_team.append( self.alive_team.pop(0))
    
    def __str__(self):
        alive = [hero.name for hero in self.alive_team]
        return " | ".join(alive)

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
def fetch_random_superheroes(n=10) -> Optional[dict]:
    #url = "https://akabab.github.io/superhero-api/api/all.json"
    numbers = random.sample(range(733), n)
    url = f"https://superheroapi.com/api/{API_KEY}/all.json"
    response = requests.get(url)
    # print(f"response: {response}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def populate_superheroes(heroes_data: dict = {}, n:int = 10,) -> list[Superhero]:
    """Populates superheroes from the given data."""
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


def make_layout() -> Layout:
    """Define the layout"""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    layout["side"].split(Layout(name="box1"), Layout(name="box2"))
    return layout


def render_table(team1: Team, team2: Team, simulation_actions=[]) -> Table:
    """Display the teams with their members and actions."""
    table = Table()

    table.add_column("Team 1", justify="right")
    table.add_column("Simulation", justify="center", min_width=80)
    table.add_column("Team 2", justify="right")
    table_length =  max(len(simulation_actions),5)

    for i in range(0, table_length):
        simulation_text = ""
        if i < len(simulation_actions):
            simulation_text = simulation_actions[i]
        hero1_text = team1.member_idx(i)
        hero2_text = team2.member_idx(i)
        table.add_row(hero1_text, simulation_text, hero2_text)

    return table


# Simulate the fight
def simulate_fight(team1: Team, team2: Team) -> None:
    """Simulate the fight and display updates using rich."""
    console.print("[bold magenta]Battle Begins![/bold magenta]", justify="center")

    t1_fighter = team1.next_member()
    t2_fighter = team2.next_member()
    attack_order = [(team1,team2), (team2,team1)]
    simulation_actions = []

    with Live(console=console, screen=False, auto_refresh=False) as live:
        live.update(render_table(team1, team2, simulation_actions), refresh=True) # so there's a first update on screen
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
                action = Text(f"{attacker.name} uses {attack_type} attack!  {defender.name} took {damage} damage. {defender.name} HP: {defender_hp}")
                simulation_actions.append(action)
                # if attack killed
                if defender_hp <= 0:
                    next_member_str = f"{defender.name} has died. "
                    if random_choice == 0:
                        team2.bury_member()
                        t2_fighter = team2.next_member()
                        defender = t2_fighter
                        if t2_fighter:
                            next_member_str += f"{t2_fighter.name} steps in!"
                    else:
                        team1.bury_member()
                        t1_fighter = team1.next_member()
                        defender = t1_fighter
                        if t1_fighter:
                            next_member_str += f"{t1_fighter.name} steps in!"
                    next_member_text = Text(next_member_str, style="blue bold")
                    simulation_actions.append(next_member_text)    
                time.sleep(SLEEP_TIME)
            live.update(render_table(team1, team2, simulation_actions), refresh=True)

    # Announce winner
    winner = "Team 1" if any(hero.hp > 0 for hero in team1.alive_team) else "Team 2"
    console.print(f"[bold green]Winner: {winner}[/bold green]", justify="center")


def main() -> None:
    """Main function to execute the simulation."""
    superheroes = fetch_all_superheroes()
    if superheroes:
        selected_heroes = populate_superheroes(superheroes)
        team1_data, team2_data = selected_heroes[:5], selected_heroes[5:]
        team1, team2 = Team(team1_data), Team(team2_data)
        simulate_fight(team1, team2)
    else:
        print("Failed to fetch superhero data.")

if __name__ == "__main__":
    main()



    

