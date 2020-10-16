from django.test import TestCase
from typing import Optional

from item_management.models import Stackable, Player


POTION_TYPE = 'potion'
POTION_NAME = 'Potion of Healing'
ARROW_TYPE = 'ammunition'
ARROW_NAME = 'Wooden Arrow'

class StackableModelTest(TestCase):

    def setUp(self) -> None:
        self.player = Player.objects.create(name="Nick")
        super().setUp()

    @classmethod
    def create_potions(cls, owner: Optional[Player], amount):
        if owner == None:
            owner = Player.objects.get(name__exact="Party")
        player_id = owner.id if owner else None
        return Stackable.objects.create(stackable_type=POTION_TYPE, name=POTION_NAME, quantity=amount, player_id=player_id)

    @classmethod
    def create_arrows(cls, owner: Optional[Player], amount):

        if owner == None:
            owner = Player.objects.get(name__exact="Party")
        player_id = owner.id if owner else None
        return Stackable.objects.create(stackable_type=ARROW_TYPE, name=ARROW_NAME, quantity=amount,
                                        player_id=player_id)


    def test_loose_stackable_count(self):
        nicks_potions = self.create_potions(self.player, 20)
        loose_potions = self.create_potions(None, 5)

        self.assertIs(Stackable.count_unclaimed(), loose_potions.quantity)

    def test_splitting_loose_items(self):
        loose_potions = self.create_potions(None, 15)

        ref = loose_potions.id
        new_stack = loose_potions.transfer_to_player(self.player, amount=3)

        self.assertEqual(new_stack.quantity, 3)
        self.assertEqual(loose_potions.quantity, 12)
        self.assertEqual(ref, loose_potions.id)

    def test_transfer_to_unclaimed(self):
        nicks_potions = self.create_potions(self.player, 20)
        new_stack = nicks_potions.transfer_to_party(7)

        self.assertEqual(7, new_stack.quantity)
        self.assertEqual(13, nicks_potions.quantity)

    def test_transfer_to_self(self):
        nicks_potions = self.create_potions(self.player, 5)
        nicks_potions = nicks_potions.transfer_to_player(self.player, 3)

        self.assertEqual(5, nicks_potions.quantity)

        nicks_potions = nicks_potions.transfer_to_player(self.player, 10)
        self.assertEqual(5, nicks_potions.quantity)

    def test_transfer_from_unclaimed(self):
        nicks_potions = self.create_potions(self.player, 5)
        loose_potions = self.create_potions(None, 11)
        nicks_potions = loose_potions.transfer_to_player(self.player, 2)

        self.assertEqual(7, nicks_potions.quantity)
        self.assertEqual(9, loose_potions.quantity)

    def test_transfer_different_item_types(self):
        nicks_potions = self.create_potions(self.player, 10)
        loose_potions = self.create_potions(None, 40)
        nicks_arrows = self.create_arrows(self.player, 3)
        loose_arrows = self.create_arrows(None, 51)

        loose_potions = nicks_potions.transfer_to_party(5)
        nicks_arrows = loose_arrows.transfer_to_player(self.player, 27)

        self.assertEqual(45, Stackable.objects.get(name=POTION_NAME, player__name="Party").quantity)
        self.assertEqual(5, Stackable.objects.get(name=POTION_NAME, player__name=self.player.name).quantity)
        self.assertEqual(24, Stackable.objects.get(name=ARROW_NAME, player__name="Party").quantity)
        self.assertEqual(30, Stackable.objects.get(name=ARROW_NAME, player__name=self.player).quantity)
        self.assertEqual(4, len(Stackable.objects.all()))


    def test_transfer_invalid_amount(self):
        nicks_potions = self.create_potions(self.player, 5)
        loose_potions = nicks_potions.transfer_to_party(-7)

        self.assertIsNone(loose_potions)
        self.assertEqual(5, nicks_potions.quantity)

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