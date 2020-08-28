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
    list_display = ('description', 'rarity', 'item_slot', 'requires_attunement', 'wondrous', 'player')
    list_display_links = ('description',)
    list_editable = ('requires_attunement', 'wondrous', 'player',)


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Level', {'fields': ['level']}),
        ('Description', {'fields': ['description']}),

    ]
    ordering = ('level',)


@admin.register(ItemSlot)
class ItemSlotAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Slot', {'fields': ['slot_name']}),
    ]

@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    fieldsets = ('Description', {'fields': ['description']}),

admin.site.register(Player)
admin.site.register(Description)
admin.site.register(Rarity)
