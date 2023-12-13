import requests
import random
import time
from typing import List, Optional, Tuple
import os
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from superhero import Superhero
from team import Team
from api import fetch_all_superheroes, fetch_random_superheroes

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



    
def populate_superheroes(heroes_data: dict = {}, n:int = 10,) -> list[Superhero]:
    """Populates superheroes from the given data."""
    # Convert the dictionary values to a list
    heroes_list = list(heroes_data)
    random_heroes = random.sample(heroes_list, n)

    superheroes = []
    for hero in random_heroes:
        superheroes.append(Superhero(
            MAX_FB,
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



    
