from django.forms import model_to_dict
from django.test import TestCase

from item_management.models import WeaponTrait, Tier, Player, Weapon, ItemSlot, TraitTemplate


class TraitModelTests(TestCase):

    def setUp(self):
        self.tier = Tier.objects.create(description="A tier", level=0)
        self.template = TraitTemplate.objects.create(scaling_trait=True, tier=self.tier)
        self.player = Player.objects.create(name="Nyhm")
        self.weapon_slot = ItemSlot.objects.create(slot_name="weapon")
        self.weapon = Weapon.objects.create(name="Dagger", item_slot=self.weapon_slot, player=self.player)

    def test_create_from_template(self):
        x_val = 3
        armor_piercing_template = TraitTemplate.objects.create(trait_name="Armor Piercing (X)", tier=self.tier, scaling_trait=True)

        armor_piercing_instance = WeaponTrait.create_trait_from_template(armor_piercing_template, self.weapon, 'Melee', x_value=x_val)


        self.assertNotEqual(armor_piercing_template.id, armor_piercing_instance.id)
        self.assertEqual(armor_piercing_template.trait_name, armor_piercing_instance.template.trait_name)
        self.assertEqual(armor_piercing_instance.item, self.weapon)

        self.assertEqual(x_val, armor_piercing_instance.x_value)
        self.assertNotIsInstance(armor_piercing_instance, TraitTemplate)
        self.assertEqual(armor_piercing_instance.template, armor_piercing_template)

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





