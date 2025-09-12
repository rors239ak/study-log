import json
import random

class MapEditor:
    def __init__(self, map_file):
        self.map_file = map_file
        self.load_map()

    def load_map(self):
        with open(self.map_file, 'r') as file:
            self.map_data = json.load(file)

    def save_map(self):
        with open(self.map_file, 'w') as file:
            json.dump(self.map_data, file, indent=4)

    def randomize_wizard_attack(self):
        attack_range = self.get_visible_area()
        self.map_data['wizard_attack'] = random.choice(attack_range)

    def set_assassin_attack(self):
        self.map_data['assassin_attack'] = 6  # Attack at 6 tiles ahead

    def add_objects_to_house(self):
        house_objects = ['desk', 'kitchen', 'toilet', 'bed']
        self.map_data['house_objects'] = house_objects

    def move_grassland_map(self):
        grassland_map = self.map_data.pop('grassland_area', None)
        if grassland_map:
            self.map_data['new_grassland_area'] = grassland_map

    def create_sea_area(self):
        sea_area = {
            'background': 'blue',
            'enemies': ['fish', 'shell', 'swimmer'],
            'impassable_objects': ['whirlpool'],
            'beach_area': {
                'background': 'skin_color'
            }
        }
        self.map_data['sea_area'] = sea_area

    def get_visible_area(self):
        # This function should return the visible area based on the game logic
        return [1, 2, 3, 4, 5]  # Example range

    def edit_map(self):
        self.randomize_wizard_attack()
        self.set_assassin_attack()
        self.add_objects_to_house()
        self.move_grassland_map()
        self.create_sea_area()
        self.save_map()

if __name__ == "__main__":
    editor = MapEditor('game/maps/overworld.json')
    editor.edit_map()