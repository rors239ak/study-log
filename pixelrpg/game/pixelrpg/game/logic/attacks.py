import random

class Attack:
    def __init__(self, attacker, target):
        self.attacker = attacker
        self.target = target

    def perform_attack(self):
        if self.attacker.role == 'wizard':
            damage = self.random_wizard_attack()
        elif self.attacker.role == 'assassin':
            damage = self.assassin_attack()
        else:
            damage = 0
        
        self.target.take_damage(damage)

    def random_wizard_attack(self):
        # Wizard's attack can hit randomly within the visible range
        return random.randint(5, 15)  # Example damage range

    def assassin_attack(self):
        # Assassin's attack is fixed at 6 squares ahead
        return 10  # Example fixed damage


class Character:
    def __init__(self, name, role, health):
        self.name = name
        self.role = role
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} takes {damage} damage, remaining health: {self.health}")


# Example usage
wizard = Character("Gandalf", "wizard", 100)
assassin = Character("Ezio", "assassin", 100)

# Wizard attacks
wizard_attack = Attack(wizard, assassin)
wizard_attack.perform_attack()

# Assassin attacks
assassin_attack = Attack(assassin, wizard)
assassin_attack.perform_attack()