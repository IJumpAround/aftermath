from django.forms import model_to_dict
from django.test import TestCase

from item_management.models import WeaponTrait, Tier, Player, Weapon, ItemSlot, TraitTemplate, ArmorTrait, Armor


class TraitModelTests(TestCase):

    def setUp(self):
        self.tier = Tier.objects.create(description="A tier", level=0)
        self.weapon_template = TraitTemplate.objects.create(trait_name="Some Trait (X)", scaling_trait=True, tier=self.tier)
        self.armor_template = TraitTemplate.objects.create(trait_name="Impeding (X)", scaling_trait=True, tier=self.tier)
        self.player = Player.objects.create(name="Nyhm")
        self.weapon_slot = ItemSlot.objects.create(slot_name="weapon")
        self.chest_slot = ItemSlot.objects.create(slot_name="Chest")
        self.weapon = Weapon.objects.create(name="Dagger", item_slot=self.weapon_slot, player=self.player)
        self.armor = Armor.objects.create(name="Mail Armor",item_slot=self.chest_slot, player=self.player)

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

    def test_create_armor_trait_from_template(self):
        x_value = 1
        armor_trait = ArmorTrait.create_trait_from_template(self.armor_template, self.armor, x_value=x_value)

        self.assertNotEqual(self.armor_template.id, armor_trait.id)
        self.assertEqual(self.armor_template.trait_name, armor_trait.template.trait_name)
        self.assertEqual(armor_trait.item, self.armor)


    def test_str_method_on_scalable(self):
        x_val = 4
        trait = WeaponTrait.create_trait_from_template(self.weapon_template, self.weapon, 'Melee', x_value=x_val)

        string = trait.__str__()

        self.assertEqual(f"Some Trait ({x_val}) on {trait.item}", string)

    def test_str_method_on_non_scalable(self):
        template = TraitTemplate.objects.create(trait_name="A non scaling trait", scaling_trait=False, tier=self.tier)
        trait = WeaponTrait.create_trait_from_template(template, self.weapon, 'Melee')

        string = trait.__str__()

        self.assertEqual(f"{trait.template.trait_name} on {trait.item}", string)




