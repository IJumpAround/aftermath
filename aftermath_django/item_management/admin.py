from django import forms
from django.contrib import admin
from django.db.models import TextField
from django.forms import models
from tinymce.widgets import TinyMCE

from .models import Player, Weapon, WeaponTrait, Armor, ArmorTrait, ItemSlot, Rarity, Tier, Stackable, TraitTemplate, \
    ArmorTraitTemplate, WeaponTraitTemplate


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Description', {'fields': ['name', 'flavor', 'text_description']}),
        (None, {'fields': ['rarity']}),
        (None, {'fields': ['player']}),
        (None, {'fields': ['item_slot']})
        # ('Date information', {'fields': ['pub_date']})
    ]
    list_display = ('name', 'rarity', 'item_slot', 'requires_attunement', 'is_attuned', 'player')
    list_editable = ('requires_attunement', 'is_attuned', 'player', 'item_slot', 'rarity')


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


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = '__all__'
        widgets = {
            'text_description': TinyMCE(mce_attrs={'width': '75%', 'height': 300}),
            'flavor': TinyMCE(mce_attrs={'width': '50%', 'height': 200})
        }


class WeaponTraitInline(admin.TabularInline):
    model = WeaponTrait
    extra = 0


@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    inlines = [
        WeaponTraitInline,
    ]

    form = ProjectAdminForm

    fieldsets = [('Description', {'fields': ['name', 'flavor', 'text_description']}),
                 ('Misc', {'fields': ['rarity', 'item_slot']}),
                 ('Owner', {'fields': ['player']})
                 ]
    list_display = ('name', 'rarity', 'item_slot', 'requires_attunement', 'is_attuned', 'player')
    list_editable = ('requires_attunement', 'is_attuned', 'player', 'item_slot', 'rarity')


@admin.register(Stackable)
class StackableAdmin(admin.ModelAdmin):
    fieldsets = [('Description', {'fields': ['name', 'text_description', 'stackable_type']}),
                 ('Owner', {'fields': ['player', 'quantity']})
                 ]


class TraitTemplateAdmin(admin.ModelAdmin):
    fieldsets = [('Description', {'fields': ['trait_name', 'description']}),
                 (None, {'fields': ['tier', 'scaling_trait']}),
                 ]


@admin.register(ArmorTraitTemplate)
class ArmorTraitTemplateAdmin(TraitTemplateAdmin):
    pass


@admin.register(WeaponTraitTemplate)
class WeaponTraitTemplateAdmin(TraitTemplateAdmin):
    pass


@admin.register(WeaponTrait)
class WeaponTraitAdmin(admin.ModelAdmin):
    fieldsets = [('Description', {'fields': ['template', 'weapon_type', 'x_value']}),
                 (None, {'fields': ['item']})]

    # list_display = ('template',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        non_editable = ['template', 'item']
        for key in non_editable:
            field = form.base_fields[key]
            field.widget.can_add_related = True
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return form

    class Media:
        js = ('item_management/trait_x_value_disable.js',)


@admin.register(ArmorTrait)
class ArmorTraitAdmin(admin.ModelAdmin):
    fieldsets = [('Description', {'fields': ['template', 'x_value']}),
                 (None, {'fields': ['item']})
                 ]
    list_display = ('template',)

    class Media:
        js = ('item_management/trait_x_value_disable.js',)


admin.site.register(Player)
admin.site.register(Rarity)
