import random

class EnemyAI:
    def __init__(self, position):
        self.position = position

    def wizard_attack(self):
        # 魔法使いの攻撃をブラウザに見えている範囲でランダムに設定
        attack_range = [(self.position[0] + x, self.position[1] + y) 
                        for x in range(-1, 2) 
                        for y in range(-1, 2)]
        return random.choice(attack_range)

    def assassin_attack(self):
        # 暗殺者の攻撃を前方6マス目に設定
        forward_position = (self.position[0] + 6, self.position[1])
        return forward_position

# 例: 敵のAIを初期化し、攻撃を実行
enemy_ai = EnemyAI(position=(5, 5))
wizard_attack_position = enemy_ai.wizard_attack()
assassin_attack_position = enemy_ai.assassin_attack()

print(f"Wizard attacks at: {wizard_attack_position}")
print(f"Assassin attacks at: {assassin_attack_position}")