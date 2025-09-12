from random import randint

class Enemy:
    def __init__(self, name, attack_range):
        self.name = name
        self.attack_range = attack_range

    def attack(self):
        return randint(1, self.attack_range)

class Wizard(Enemy):
    def __init__(self):
        super().__init__("Wizard", 10)  # Wizard can attack randomly within a range of 1 to 10

class Assassin(Enemy):
    def __init__(self):
        super().__init__("Assassin", 5)  # Assassin attacks at a fixed range of 6 squares ahead

    def attack(self):
        return 6  # Fixed attack range for the Assassin

class Fish(Enemy):
    def __init__(self):
        super().__init__("Fish", 3)  # Fish can attack randomly within a range of 1 to 3

class Shell(Enemy):
    def __init__(self):
        super().__init__("Shell", 2)  # Shell can attack randomly within a range of 1 to 2

class Swimmer(Enemy):
    def __init__(self):
        super().__init__("Swimmer", 4)  # Swimmer can attack randomly within a range of 1 to 4

# Example of how to use the classes
def enemy_attack_example():
    wizard = Wizard()
    assassin = Assassin()
    fish = Fish()
    shell = Shell()
    swimmer = Swimmer()

    print(f"{wizard.name} attacks with damage: {wizard.attack()}")
    print(f"{assassin.name} attacks with damage: {assassin.attack()}")
    print(f"{fish.name} attacks with damage: {fish.attack()}")
    print(f"{shell.name} attacks with damage: {shell.attack()}")
    print(f"{swimmer.name} attacks with damage: {swimmer.attack()}")