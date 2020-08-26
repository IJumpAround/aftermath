from django.contrib import admin

from .models import Player, Weapon, WeaponTrait, Armor, ArmorTrait, ItemSlot, Rarity, Description, Tier


class ArmorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Description',      {'fields': ['description']}),
        (None,               {'fields': ['rarity']}),
        (None,               {'fields': ['player']})
        # ('Date information', {'fields': ['pub_date']})
    ]


# # class ChoiceAdmin(admin.ModelAdmin):
# #     fieldsets = [
# #         ()
# #     ]

# admin.site.register(Question, QuestionAdmin)
admin.site.register(Player)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Description)
admin.site.register(Rarity)