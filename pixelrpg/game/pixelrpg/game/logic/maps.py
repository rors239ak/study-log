from random import choice, randint

class Map:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.objects = []
        self.enemies = []

    def add_object(self, obj):
        self.objects.append(obj)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

class Grassland(Map):
    def __init__(self):
        super().__init__("Grassland", 20, 15)
        self.add_object("grass")
        self.add_object("tree")
        self.add_object("rock")

class HouseInterior(Map):
    def __init__(self):
        super().__init__("House Interior", 10, 10)
        self.add_object("table")
        self.add_object("kitchen")
        self.add_object("toilet")
        self.add_object("bed")

class SeaArea(Map):
    def __init__(self):
        super().__init__("Sea Area", 30, 20)
        self.add_object("whirlpool")
        self.add_enemy("fish")
        self.add_enemy("shell")
        self.add_enemy("swimmer")

class BeachArea(Map):
    def __init__(self):
        super().__init__("Beach Area", 25, 15)
        self.add_object("sand")
        self.add_object("beach_umbrella")

def get_random_attack_range():
    return randint(1, 6)

def get_assassin_attack_position():
    return 6  # Fixed position for assassin attack

def main():
    grassland = Grassland()
    house_interior = HouseInterior()
    sea_area = SeaArea()
    beach_area = BeachArea()

    print(f"Grassland Objects: {grassland.objects}")
    print(f"House Interior Objects: {house_interior.objects}")
    print(f"Sea Area Enemies: {sea_area.enemies}")
    print(f"Beach Area Objects: {beach_area.objects}")

    # Example of random attack for wizard
    wizard_attack_range = get_random_attack_range()
    print(f"Wizard attack range: {wizard_attack_range}")

    # Example of fixed attack for assassin
    assassin_attack_position = get_assassin_attack_position()
    print(f"Assassin attack position: {assassin_attack_position}")

if __name__ == "__main__":
    main()