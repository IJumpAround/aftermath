from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import model_to_dict
from django.test import TestCase

from item_management.models import WeaponTrait, Tier, Player, Weapon, ItemSlot, TraitTemplate, ArmorTrait, Armor, \
    WeaponTraitTemplate, ArmorTraitTemplate


class TraitModelTests(TestCase):

    def setUp(self):
        self.tier = Tier.objects.create(description="A tier", level=0)
        self.weapon_template = WeaponTraitTemplate.objects.create(trait_name="Some Trait (X)", scaling_trait=True, tier=self.tier, trait_type='Weapon')
        self.armor_template = ArmorTraitTemplate.objects.create(trait_name="Impeding (X)", scaling_trait=True, tier=self.tier, trait_type='Armor')
        self.player = Player.objects.create(name="Nyhm")
        self.weapon_slot = ItemSlot.objects.create(slot_name="weapon")
        self.chest_slot = ItemSlot.objects.create(slot_name="Chest")
        self.weapon = Weapon.objects.create(name="Dagger", item_slot=self.weapon_slot, player=self.player)
        self.armor = Armor.objects.create(name="Mail Armor",item_slot=self.chest_slot, player=self.player)

    def test_create_from_template(self):
        x_val = 3
        armor_piercing_template = WeaponTraitTemplate.objects.create(trait_name="Armor Piercing (X)", tier=self.tier, scaling_trait=True, trait_type='Weapon')

        armor_piercing_instance = WeaponTrait.create_trait_from_template(armor_piercing_template, self.weapon, weapon_type='Melee', x_value=x_val)


        self.assertEqual(armor_piercing_template.trait_name, armor_piercing_instance.template.trait_name)
        self.assertEqual(armor_piercing_instance.item, self.weapon)

        self.assertNotIsInstance(armor_piercing_instance, TraitTemplate)
        self.assertEqual(armor_piercing_instance.template, armor_piercing_template)

    def test_create_armor_trait_from_template(self):
        x_value = 1
        armor_trait = ArmorTrait.create_trait_from_template(self.armor_template, self.armor, x_value=x_value)

        self.assertEqual(self.armor_template.trait_name, armor_trait.template.trait_name)
        self.assertEqual(armor_trait.item, self.armor)


    def test_str_method_on_scalable(self):
        x_val = 4
        trait = WeaponTrait.create_trait_from_template(self.weapon_template, self.weapon, weapon_type='Melee', x_value=x_val)

        string = trait.__str__()

        self.assertEqual(f"Some Trait ({x_val}) on {trait.item}", string)

    def test_str_method_on_non_scalable(self):
        template = WeaponTraitTemplate.objects.create(trait_name="A non scaling trait", scaling_trait=False, tier=self.tier, trait_type='Weapon')
        trait = WeaponTrait.create_trait_from_template(template, self.weapon, weapon_type='Melee')

        string = trait.__str__()

        self.assertEqual(f"{trait.template.trait_name} on {trait.item}", string)

    def test_scalable_requires_x_value(self):
        with self.assertRaises(ValidationError):
            armor_trait = self.armor_template.create_trait_from_template(item=self.weapon)

    def test_trait_creation_from_template_classmethod(self):
        armor_trait = self.armor_template.create_trait_from_template(item=self.weapon, x_value=3)
        weapon_trait = self.weapon_template.create_trait_from_template(item=self.armor, x_value=2, weapon_type='Melee')

        self.assertEqual(self.armor_template.trait_name, armor_trait.template.trait_name)
        self.assertEqual(armor_trait.item, self.armor)

        self.assertEqual(self.weapon_template.trait_name, weapon_trait.template.trait_name)
        self.assertEqual(weapon_trait.item, self.weapon)

    def test_item_can_have_multiple_traits(self):
        weapon_template2 = WeaponTraitTemplate.objects.create(trait_name="Another Weapon Trait", scaling_trait=False, tier=self.tier, trait_type='Weapon')
        weapon_trait = self.weapon_template.create_trait_from_template(item=self.weapon, x_value=2, weapon_type='Melee')
        weapon_trait2 = weapon_template2.create_trait_from_template(item=self.weapon, weapon_type='Melee')

        traits = self.weapon.weapontrait_set.all()
        print('test')

        self.assertIn(weapon_trait, traits)
        self.assertIn(weapon_trait2, traits)


