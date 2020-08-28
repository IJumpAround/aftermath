from django.contrib import admin

from .models import Player, Weapon, WeaponTrait, Armor, ArmorTrait, ItemSlot, Rarity, Description, Tier


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Description', {'fields': ['description']}),
        (None, {'fields': ['rarity']}),
        (None, {'fields': ['player']})
        # ('Date information', {'fields': ['pub_date']})
    ]


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Level', {'fields': ['level']}),
        ('Description', {'fields': ['description']}),

    ]
    ordering = ('level',)


admin.site.register(Player)
admin.site.register(Description)
admin.site.register(Rarity)
