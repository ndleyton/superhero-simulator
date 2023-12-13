import math
from typing import Tuple
import random


class Superhero:
    """Class representing a Superhero with necessary attributes and methods to fight and keep track of health"""
    def __init__(self, fb_random_max, name, intelligence, strength, speed, durability, power, combat, alignment, image=''):
        # set the setting or random dependant attributes
        self.team_alignment = None
        self.fb = None
        self.actual_stamina : int = random.randint(0,9)
        self.fb_random : int = random.randint(0, fb_random_max)
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