from django.test import TestCase

from item_management.models import Stackable, Player


class StackableModelTest(TestCase):

    def test_loose_stackable_count(self):
        player = Player.objects.create(name="Nick")
        nicks_potions = Stackable.objects.create(stackable_type='potion', name='Potion of Healing', quantity=20, player_id=player.id)
        loose_potions = Stackable.objects.create(stackable_type='potion', name='Potion of Healing', quantity=5)

        self.assertIs(Stackable.count_unclaimed(), loose_potions.quantity)


    def test_splitting_loose_items(self):
        player = Player.objects.create(name="Nick")
        loose_potions = Stackable.objects.create(stackable_type='potion', name='Potion of Healing', quantity=15)

        ref = loose_potions.id
        new_stack = loose_potions.transfer(player_name=player.name, amount=3)

        self.assertEqual(new_stack.quantity, 3)
        self.assertEqual(loose_potions.quantity, 12)
        self.assertEqual(ref, loose_potions.id)

    def test_transfer_to_unclaimed(self):
        raise NotImplemented

    def test_split_to_existing_stack_combines(self):
        raise NotImplemented

    def test_transfer_more_than_available(self):
        raise NotImplemented

    def test_transfer_all(self):
        raise NotImplemented