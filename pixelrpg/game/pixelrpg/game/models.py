from django.db import models
import random

class Character(models.Model):
    name = models.CharField(max_length=100)
    health = models.IntegerField()
    attack_power = models.IntegerField()

    def attack(self, target):
        damage = self.attack_power
        if self.name == "Wizard":
            damage = random.randint(5, 15)  # Wizard's attack is random
        target.health -= damage
        target.save()

class Assassin(Character):
    def attack(self, target):
        # Attack is fixed at 6 spaces ahead
        target.health -= self.attack_power
        target.save()

class Enemy(models.Model):
    name = models.CharField(max_length=100)
    health = models.IntegerField()
    attack_power = models.IntegerField()

class Fish(Enemy):
    pass

class Shell(Enemy):
    pass

class Swimmer(Enemy):
    pass

class HouseObject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Kitchen(HouseObject):
    pass

class Table(HouseObject):
    pass

class Toilet(HouseObject):
    pass

class Bed(HouseObject):
    pass

class Map(models.Model):
    name = models.CharField(max_length=100)
    layout = models.JSONField()  # Store map layout as JSON

class Grassland(Map):
    pass

class Sea(Map):
    pass

class Beach(Map):
    pass

class Whirlpool(models.Model):
    position = models.CharField(max_length=100)  # Position on the map
    is_passable = models.BooleanField(default=False)  # Cannot pass through whirlpool