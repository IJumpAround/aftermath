from django.forms import model_to_dict
from django.test import TestCase

from item_management.models import WeaponTrait, Tier, Player, Weapon, ItemSlot


class TraitModelTests(TestCase):

    def setUp(self):
        self.tier = Tier.objects.create(description="A tier", level=0)
        self.player = Player.objects.create(name="Nyhm")
        self.weapon_slot = ItemSlot.objects.create(slot_name="weapon")
        self.weapon = Weapon.objects.create(name="Dagger", item_slot=self.weapon_slot, player=self.player)


    def create_weapon_trait(self, name="Accurate", weapon_type='Melee', tier=None):
        if not tier:
            tier = self.tier

        return WeaponTrait.objects.create(trait_name=name, weapon_type='Melee', tier=self.tier, is_template=True)


    def test_create_from_template(self):
        x_val = 3
        armor_piercing_template = WeaponTrait.objects.create(trait_name="Armor Piercing (X)", is_template=True, weapon_type='Melee', tier=self.tier)

        armor_piercing_instance = WeaponTrait.create_trait_from_template(armor_piercing_template, self.weapon, 'Melee', x_value=x_val)


        self.assertNotEqual(armor_piercing_template.id, armor_piercing_instance.id)
        self.assertEqual(armor_piercing_template.trait_name, armor_piercing_instance.trait_name)
        self.assertEqual(armor_piercing_instance.item, self.weapon)

        self.assertEqual(x_val, armor_piercing_instance.x_value)
        self.assertIsNone(armor_piercing_template.x_value)
        self.assertFalse(armor_piercing_instance.is_template)
        self.assertTrue(armor_piercing_template.is_template)

    def test_get_templates_only_returns_templates(self):
        x_val = 2
        armor_piercing_template = WeaponTrait.objects.create(trait_name="Armor Piercing (X)", is_template=True, weapon_type='Melee', tier=self.tier)
        acrobatic = WeaponTrait.objects.create(trait_name="Acrobatic", is_template=True, weapon_type='Melee', tier=self.tier)
        armor_piercing_instance = WeaponTrait.create_trait_from_template(armor_piercing_template, self.weapon, 'Melee', x_value=x_val)

        results = WeaponTrait.get_templates()
        print(results)
        self.assertEqual(2, len(results))
        self.assertIn(armor_piercing_template, results)
        self.assertIn(acrobatic, results)





