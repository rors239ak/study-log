from django.contrib import admin
from .models import Enemy, Attack, GameObject

class EnemyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'health', 'attack_power')
    search_fields = ('name',)

class AttackAdmin(admin.ModelAdmin):
    list_display = ('name', 'damage', 'range', 'element')
    search_fields = ('name',)

class GameObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'object_type', 'position')
    search_fields = ('name',)

admin.site.register(Enemy, EnemyAdmin)
admin.site.register(Attack, AttackAdmin)
admin.site.register(GameObject, GameObjectAdmin)