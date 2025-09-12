from django.test import TestCase
from game.logic.enemies import Assassin, Wizard
from game.logic.attacks import MagicAttack, PhysicalAttack

class AttackTestCase(TestCase):
    def setUp(self):
        self.wizard = Wizard()
        self.assassin = Assassin()

    def test_wizard_attack_random_range(self):
        damage = self.wizard.cast_spell()
        self.assertIn(damage, range(5, 15))  # Assuming wizard's attack damage is between 5 and 15

    def test_assassin_attack_fixed_range(self):
        damage = self.assassin.attack(target_distance=6)
        self.assertEqual(damage, 10)  # Assuming assassin's attack damage at 6 tiles is fixed at 10

class GameObjectTestCase(TestCase):
    def test_house_objects(self):
        house_objects = ['desk', 'kitchen', 'toilet', 'bed']
        for obj in house_objects:
            self.assertIn(obj, self.assassin.get_house_objects())

class SeaAreaTestCase(TestCase):
    def test_sea_area_enemies(self):
        sea_enemies = ['fish', 'shell', 'swimmer']
        for enemy in sea_enemies:
            self.assertIn(enemy, self.wizard.get_sea_enemies())

    def test_whirlpool_obstacle(self):
        self.assertTrue(self.wizard.can_pass('whirlpool'), False)  # Assuming whirlpool is an impassable object

    def test_background_color(self):
        self.assertEqual(self.wizard.get_background_color(), 'blue')  # Assuming the background color is blue for the sea area

    def test_beach_area_color(self):
        self.assertEqual(self.wizard.get_beach_color(), 'skin')  # Assuming the beach area is represented by skin color