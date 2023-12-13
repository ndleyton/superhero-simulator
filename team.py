from typing import Optional
from rich.text import Text
from superhero import Superhero


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