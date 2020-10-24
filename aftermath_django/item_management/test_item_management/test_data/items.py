from django.test import TestCase

from item_management.models import Weapon, ItemSlot, Player, Armor, Stackable


def add_test_data_to_class(ref: TestCase):
    """
    Creates item attributes on the testcase class
    Args:
        ref: reference to the class, pass the testcase classes ref to this function

    Creates new attributes on the test class
    """
    ref.player = Player.objects.create(name="Nyhm")
    ref.weapon_slot = ItemSlot.objects.create(slot_name="weapon")
    ref.chest_slot = ItemSlot.objects.create(slot_name="Chest")
    ref.weapon = Weapon.objects.create(name="Dagger", item_slot=ref.weapon_slot, player=ref.player)
    ref.armor = Armor.objects.create(name="Mail Armor", item_slot=ref.chest_slot, player=ref.player)
    ref.potions = Stackable.objects.create(name="Potion of Healing", stackable_type="Potion", quantity=30)
    ref.arrows = Stackable.objects.create(name="Arrows", stackable_type="Ammunition", quantity=15)