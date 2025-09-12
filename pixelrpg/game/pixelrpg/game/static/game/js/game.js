const game = {
    characters: {
        wizard: {
            attack: function() {
                const attackRange = this.getRandomAttackRange();
                // Wizard attack logic using attackRange
            },
            getRandomAttackRange: function() {
                return Math.floor(Math.random() * 10); // Random range for wizard attack
            }
        },
        assassin: {
            attack: function() {
                const attackPosition = this.getAttackPosition();
                // Assassin attack logic using attackPosition
            },
            getAttackPosition: function() {
                return 6; // Fixed attack position for assassin
            }
        }
    },
    objects: {
        house: {
            furniture: ['desk', 'kitchen', 'toilet', 'bed'],
            addObject: function(object) {
                this.furniture.push(object);
            }
        }
    },
    maps: {
        grassland: {
            moveToNewArea: function() {
                // Logic to move grassland map to a different area
            }
        },
        sea: {
            enemies: ['fish', 'shell', 'swimmer'],
            createWhirlpool: function() {
                // Logic to create an impassable whirlpool object
            },
            background: 'blue', // Sea background color
            beachArea: {
                color: 'skin', // Beach area color
            }
        }
    }
};

// Example usage
game.characters.wizard.attack();
game.characters.assassin.attack();
game.objects.house.addObject('table');
game.maps.grassland.moveToNewArea();
game.maps.sea.createWhirlpool();