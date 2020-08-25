from django.contrib import admin

from .models import Player, Weapon, WeaponTrait, Armor, ArmorTrait, ItemSlot, Rarity, Description, Tier


# class ArmorAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']})
#     ]
#
#
# # class ChoiceAdmin(admin.ModelAdmin):
# #     fieldsets = [
# #         ()
# #     ]

# admin.site.register(Question, QuestionAdmin)
admin.site.register(Player)
admin.site.register(Armor)