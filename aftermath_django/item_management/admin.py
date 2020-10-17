from django.contrib import admin

from .models import Player, Weapon, WeaponTrait, Armor, ArmorTrait, ItemSlot, Rarity, Tier, Stackable


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Description', {'fields': ['name', 'flavor', 'text_description']}),
        (None, {'fields': ['rarity']}),
        (None, {'fields': ['player']}),
        (None, {'fields': ['item_slot']})
        # ('Date information', {'fields': ['pub_date']})
    ]
    list_display = ('name', 'rarity', 'item_slot', 'requires_attunement', 'wondrous', 'player')
    list_editable = ('requires_attunement', 'wondrous', 'player','item_slot', 'rarity')

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
    fieldsets = [('Description', {'fields': ['name', 'flavor', 'text_description']}),
                 ('Misc', {'fields': ['rarity', 'item_slot']}),
                 ('Owner', {'fields': ['player']})
                 ]

@admin.register(Stackable)
class StackableAdmin(admin.ModelAdmin):
    fieldsets = [('Description', {'fields': ['name', 'text_description', 'stackable_type']}),
                 ('Owner', {'fields': ['player', 'quantity']})
                 ]

@admin.register(WeaponTrait)
class WeaponTraitAdmin(admin.ModelAdmin):
    fieldsets = [('Description', {'fields': ['trait_name', 'description', 'x_value', 'is_template']}),
                 (None, {'fields': ['tier', 'weapon_type']}),
                 (None, {'fields': ['item']})]

@admin.register(ArmorTrait)
class ArmorTraitAdmin(admin.ModelAdmin):
    fieldsets = [('Description', {'fields': ['trait_name', 'description', 'x_value', 'is_template']}),
                 (None, {'fields': ['tier']}),
                 (None, {'fields': ['item']})
                  ]

admin.site.register(Player)
admin.site.register(Rarity)
