from typing import Optional

from django.contrib import admin

from .forms import ProjectAdminForm
from .models import Player, Weapon, WeaponTrait, Armor, ArmorTrait, ItemSlot, Rarity, Tier, Stackable, \
    ArmorTraitTemplate, WeaponTraitTemplate, TraitInstanceBase


class EquippableItemAdminBase(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'item_slot', 'requires_attunement', 'is_attuned', 'is_equipped', 'player')
    list_editable = ('requires_attunement', 'is_attuned', 'player', 'item_slot', 'is_attuned', 'is_equipped', 'rarity')

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
    form = ProjectAdminForm


@admin.register(Weapon)
class WeaponAdmin(EquippableItemAdminBase):
    inlines = [WeaponTraitInline]
    form = ProjectAdminForm


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
    fieldsets = [(None, {'fields': ('weapon_type',)})]
    fieldsets.insert(0, TraitTemplateAdmin.fieldsets[0])
    fieldsets.insert(1, TraitTemplateAdmin.fieldsets[1])


@admin.register(WeaponTrait)
class WeaponTraitAdmin(admin.ModelAdmin):
    list_display = ('template',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        non_editable = ['template', 'item']
        for key in non_editable:
            field = form.base_fields[key]
            field.widget.can_add_related = True
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return form

    def get_fieldsets(self, request, obj: Optional[TraitInstanceBase] = None):
        """Exclude x_value for traits that are not scalable"""
        fieldsets = [('Description', {'fields': ['template']}),
                     (None, {'fields': ['item']})]

        if obj and obj.template.scaling_trait:
            fieldsets[0][1]['fields'].append('x_value')

        return fieldsets


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
