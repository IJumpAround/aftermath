from django.test import TestCase
from typing import Optional

from item_management.models import Stackable, Player


class StackableModelTest(TestCase):

    def setUp(self) -> None:
        self.player = Player.objects.create(name="Nick")
        super().setUp()


    def create_potions(self, owner: Optional[Player], amount):
        player_id = owner.id if owner else None
        return Stackable.objects.create(stackable_type='potion', name='Potion of Healing', quantity=amount, player_id=player_id)


    def test_loose_stackable_count(self):
        nicks_potions = self.create_potions(self.player, 20)
        loose_potions = self.create_potions(None, 5)

        self.assertIs(Stackable.count_unclaimed(), loose_potions.quantity)


    def test_splitting_loose_items(self):
        loose_potions = Stackable.objects.create(stackable_type='potion', name='Potion of Healing', quantity=15)

        ref = loose_potions.id
        new_stack = loose_potions.transfer_to_player(player_name=self.player.name, amount=3)

        self.assertEqual(new_stack.quantity, 3)
        self.assertEqual(loose_potions.quantity, 12)
        self.assertEqual(ref, loose_potions.id)


    def test_transfer_to_unclaimed(self):
        nicks_potions = Stackable.objects.create(stackable_type='potion', name='Potion of Healing', quantity=20, player_id=self.player.id)
        new_stack = nicks_potions.transfer_to_party(7)

        self.assertEqual(7, new_stack.quantity)
        self.assertEqual(13, nicks_potions.quantity)


    def test_transfer_to_existing_stack_combines(self):
        self.create_potions(None, 15)
        nicks_potions = self.create_potions(self.player, 20)

        loose_potions = nicks_potions.transfer_to_party(10)

        self.assertEqual(25 ,loose_potions.quantity)
        self.assertEqual(10, nicks_potions.quantity)


    def test_transfer_more_than_available_clamps_to_available_amount(self):
        nicks_potions = self.create_potions(self.player, 10)
        result = nicks_potions.transfer_to_party(222)

        self.assertEqual(result.quantity, 10)
        self.assertIsNone(nicks_potions.id)

    def test_transfer_all(self):
        nicks_potions = self.create_potions(self.player, 10)
        result = nicks_potions.transfer_to_party(10)

        # nicks_potions.refresh_from_db()
        self.assertEqual(result.quantity, 10)
        self.assertIsNone(nicks_potions.id)
        self.assertEqual(0, nicks_potions.quantity)