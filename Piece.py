
from random import randint


class Piece:
    team = 'n/a'
    sides = 0
    health = 0
    pos = (-1, -1)

    def __init__(self, sides, team):
        self.team = team
        self.sides = sides
        self.health = randint(1, sides)

    def __str__(self):
        return str({'sides': self.sides, 'health': self.health, 'position': self.pos, 'team': self.team})

    def get_health(self):
        return self.health

    def damage(self):
        self.health -= 1

    def is_dead(self):
        return self.health <= 0

    def move(self, newpos):
        self.pos = newpos

    def get_pos(self):
        return self.pos

    def get_team(self):
        return self.team


