class GameObject:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class Table(GameObject):
    def __init__(self, position):
        super().__init__("Table", position)

class Kitchen(GameObject):
    def __init__(self, position):
        super().__init__("Kitchen", position)

class Toilet(GameObject):
    def __init__(self, position):
        super().__init__("Toilet", position)

class Bed(GameObject):
    def __init__(self, position):
        super().__init__("Bed", position)

class SeaObject(GameObject):
    def __init__(self, name, position):
        super().__init__(name, position)

class Fish(SeaObject):
    def __init__(self, position):
        super().__init__("Fish", position)

class Shell(SeaObject):
    def __init__(self, position):
        super().__init__("Shell", position)

class Swimmer(SeaObject):
    def __init__(self, position):
        super().__init__("Swimmer", position)

class Whirlpool(GameObject):
    def __init__(self, position):
        super().__init__("Whirlpool", position)

class Grassland:
    def __init__(self):
        self.objects = [
            Table((1, 1)),
            Kitchen((2, 1)),
            Toilet((3, 1)),
            Bed((4, 1))
        ]

class SeaArea:
    def __init__(self):
        self.objects = [
            Fish((5, 5)),
            Shell((6, 5)),
            Swimmer((7, 5)),
            Whirlpool((8, 5))
        ]