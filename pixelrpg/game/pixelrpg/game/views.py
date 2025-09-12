from django.shortcuts import render
from django.http import JsonResponse
import random

# 魔法使いの攻撃をランダムに設定
def wizard_attack(request):
    attack_options = ['fireball', 'ice shard', 'lightning bolt']
    attack = random.choice(attack_options)
    return JsonResponse({'attack': attack})

# 暗殺者の攻撃を前方6マス目に設定
def assassin_attack(request):
    attack_position = 6  # 前方6マス目
    return JsonResponse({'attack_position': attack_position})

# ゲームのメインページを表示
def index(request):
    return render(request, 'game/index.html')