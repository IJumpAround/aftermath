from typing import Optional

from django.contrib import admin

from .forms import MceTextAdminForm
from .models import Player, Weapon, WeaponTrait, Armor, ArmorTrait, ItemSlot, Rarity, Tier, Stackable, \
    ArmorTraitTemplate, WeaponTraitTemplate, TraitInstanceBase


class MyAdminBase(admin.ModelAdmin):
    form = MceTextAdminForm

    def get_form(self, request, obj=None, **kwargs):
        """Make related fields selectable, but not editable"""
        form = super().get_form(request, obj, **kwargs)

        for field_name in form.base_fields:
            field = form.base_fields[field_name]
            if hasattr(field, 'to_field_name'):
                print(field)
                field.widget.can_add_related = True
                field.widget.can_change_related = False
                field.widget.can_delete_related = False
        return form


class EquippableItemAdminBase(MyAdminBase):
    list_display = ('name', 'rarity', 'item_slot', 'requires_attunement', 'is_attuned', 'is_equipped', 'player')
    list_editable = ('requires_attunement', 'is_attuned', 'is_equipped')

    def get_fieldsets(self, request, obj=None):
        item_type_name = self.model.__name__
        return [
            (item_type_name, {'fields': ['name', 'player', 'flavor', 'text_description']}),
            ('Misc', {'fields': ['rarity', 'item_slot', 'is_attuned', 'is_equipped', 'requires_attunement']}),
        ]


class TraitInlineBase(admin.TabularInline):
    extra = 0
    fields = ['template']
    readonly_fields = ('template',)


class WeaponTraitInline(TraitInlineBase):
    model = WeaponTrait


class ArmorTraitInline(TraitInlineBase):
    model = ArmorTrait


@admin.register(Armor)
class ArmorAdmin(EquippableItemAdminBase):
    inlines = [ArmorTraitInline]
    form = MceTextAdminForm


@admin.register(Weapon)
class WeaponAdmin(EquippableItemAdminBase):
    inlines = [WeaponTraitInline]
    form = MceTextAdminForm


@admin.register(Tier)
class TierAdmin(MyAdminBase):
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


@admin.register(Stackable)
class StackableAdmin(MyAdminBase):
    list_display = ('name_with_quantity', 'player',)
    fieldsets = [('Description', {'fields': ['name', 'text_description', 'stackable_type']}),
                 ('Owner', {'fields': ['player', 'quantity']})
                 ]


class TraitTemplateAdmin(MyAdminBase):
    fieldsets = [('Description', {'fields': ['trait_name', 'description']}),
                 (None, {'fields': ['tier', 'scaling_trait']}),
                 ]


@admin.register(ArmorTraitTemplate)
class ArmorTraitTemplateAdmin(TraitTemplateAdmin):
    pass


@admin.register(WeaponTraitTemplate)
class WeaponTraitTemplateAdmin(TraitTemplateAdmin):
    """Makes sure weapon_type gets added to fieldsets"""
    fieldsets = [(None, {'fields': ('weapon_type',)})]
    for i, fieldset in enumerate(TraitTemplateAdmin.fieldsets):
        fieldsets.insert(i, fieldset)


class TraitInstanceBaseAdmin(MyAdminBase):
    list_display = ('__str__', 'template', 'x_value')

    def get_fieldsets(self, request, obj: Optional[TraitInstanceBase] = None):
        """Exclude x_value for traits that are not scalable"""
        fieldsets = [('Description', {'fields': ['template']}),
                     (None, {'fields': ['item']})]

        if obj and obj.template.scaling_trait:
            fieldsets[0][1]['fields'].append('x_value')

        return fieldsets


@admin.register(WeaponTrait)
class WeaponTraitAdmin(TraitInstanceBaseAdmin):
    pass


@admin.register(ArmorTrait)
class ArmorTraitAdmin(TraitInstanceBaseAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(MyAdminBase):
    list_display = ('name', )


admin.site.register(Rarity)
