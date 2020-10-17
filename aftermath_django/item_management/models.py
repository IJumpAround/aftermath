from __future__ import annotations

from copy import deepcopy
from typing import Optional, Union

from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Count, Q, ObjectDoesNotExist
from rest_framework import serializers


class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)
    attunement_slots = models.PositiveSmallIntegerField(validators=(MaxValueValidator(limit_value=3),),
                                                        default=3,
                                                        blank=True)
    copper = models.IntegerField(blank=False,
                                 default=0)
    silver = models.IntegerField(blank=False,
                                 default=0)
    electrum = models.IntegerField(blank=False,
                                 default=0)
    gold = models.IntegerField(blank=False,
                                   default=0)
    platinum = models.IntegerField(blank=False,
                                   default=0)

    @classmethod
    def get_party(cls):
        return cls.objects.get(name="Party")

    @classmethod
    def get_default(cls):
        party = cls.objects.get_or_create(name="Party", defaults={'name':"Party"})
        return party[0].pk

    def get_items(self):
        armor = Armor.objects.filter(player_id=self.id)
        return armor

    def __str__(self):
        return self.name
    # Items
    # Effects

class ItemSlot(models.Model):
    slot_name = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return self.slot_name


class Rarity(models.Model):
    class Meta:
        verbose_name_plural = 'Rarities'

    rarity_level = models.CharField(max_length=40,
                                    unique=True)

    def __str__(self):
        return self.rarity_level


class Item(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=70)
    text_description = models.TextField()
    flavor = models.TextField(null=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    wondrous = models.BooleanField(default=False)
    requires_attunement = models.BooleanField(default=False)

    player = models.ForeignKey(Player,
                               on_delete=models.PROTECT,
                               default=Player.get_default,
                               blank=False,
                               null=False)


    @classmethod
    def get_serializer(cls):
        class BaseSerializer(serializers.ModelSerializer):

            class Meta:
                model = cls
                fields = '__all__'
                depth = 1

        return BaseSerializer


class Stackable(Item):
    # Potion, Arrows, bolts, etc
    stackable_type = models.CharField(blank=False,
                                      max_length=45)
    quantity = models.IntegerField(default=0)
    @classmethod
    def count_group_by_players(cls):
        counts = Stackable.objects.values('player_id').annotate(total=Count('id'))
        return counts
    @classmethod
    def count_for_by_player(cls, player_name) -> int:
        count = Stackable.objects.filter(player__name=player_name).count()
        return count

    @classmethod
    def count_unclaimed(cls) -> int:
        item = Stackable.objects.get(Q(player__name="Party"))
        count = item.quantity
        return count

    def transfer_to_party(self, amount):
        party = Player.objects.get(name="Party")
        return self._transfer(player=party, amount=amount)

    def transfer_to_player(self, player: Optional[Player], amount):
        return self._transfer(player, amount)

    def _transfer(self, player, amount) -> 'Stackable':
        """
        Transfer some quantity of a stack of items to a new owner
        Transferring all items in a stack will result in deletion of the source stack
        Transferring items to an existing stack will not update existing object references, as such you should either
            assign the result of this call to the target object, or call refresh_from_db on the target Stackable
        Args:
            player: Recipient of transfer.
                         Provide None to transfer to the party
            amount: Number of items to transfer to the target player

        Returns: The newly created Stackable object owned by player_name


        """
        new_owner_id = None
        if player:
            new_owner_id = Player.objects.get(name__exact=player).id

        if  amount > 0:
            if amount >= self.quantity:
                actual_amount = self.quantity
            else:
                actual_amount = amount

            self.quantity -= actual_amount
            if self.quantity == 0:
                self.delete()
            else:
                self.save()

            try:
                target_stack = Stackable.objects.get(player_id=new_owner_id, name=self.name)
            except ObjectDoesNotExist:
                target_stack = Stackable.objects.create(player_id=new_owner_id)

            target_stack.quantity += actual_amount
            target_stack.save()
            target_stack.refresh_from_db()
            return target_stack
    def __str__(self):
        return f"{self.name} x {self.quantity}: {self.player}"


class Equippable(Item):
    item_slot = models.ForeignKey(ItemSlot,
                                  on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class Armor(Equippable):
    pass

    class Meta:
        verbose_name_plural = "Armor"

    def __str__(self):
        return self.name


class Weapon(Equippable):
    pass

    def __str__(self):
        return self.name


class Tier(models.Model):
    description = models.TextField(max_length=125)
    level = models.SmallIntegerField(unique=True)

    def __str__(self):
        return f"Tier {self.level}: {self.description}"


class Trait(models.Model):
    trait_name = models.CharField(max_length=30)
    x_value = models.PositiveSmallIntegerField(null=True,
                                               blank=True)
    description = models.CharField(max_length=140)

    tier = models.ForeignKey(Tier,
                             on_delete=models.PROTECT,
                             null=False,
                             default=0)

    # Only x scalable traits will be templates
    is_template = models.BooleanField(default=False,
                                      null=False,
                                      blank=False
                                      )

    #@classmethod

    @classmethod
    def _create_trait_from_template(cls, trait: Union[WeaponTrait, ArmorTrait, int], item: Union[int, Item], x_value: int=None) -> Union[WeaponTrait, ArmorTrait]:
        if isinstance(trait, int):
            trait = cls.objects.get(tier_id=id)

        if isinstance(item, Item):
            item = item.id

        trait = deepcopy(trait)
        trait.is_template = False
        trait.x_value = x_value
        trait.item_id  = item
        trait.id = None

        return trait

    @classmethod
    def get_templates(cls):
        return cls.objects.filter(is_template=True)

    class Meta:
        abstract = True

    def __str__(self):
        trait_name = self.trait_name
        if "(X)" in trait_name:
            trait_name = f'{trait_name[:trait_name.index("(X)")]} ({self.x_value})'
        return f"{trait_name}"

class ArmorTrait(Trait):
    item = models.ForeignKey(Armor, on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             default=None)

    @classmethod
    def create_trait_from_template(cls, trait: Union[WeaponTrait, ArmorTrait, int], item: Union[int, Item], x_value: int=None) ->ArmorTrait:
        new_trait = super()._create_trait_from_template(trait, item, x_value)

        return new_trait

    def __str__(self):
        return f"{super().__str__()} on {self.item}"


class WeaponTrait(Trait):
    class WeaponType(models.TextChoices):
        SPECIAL = 'Special'
        EITHER = 'Either'
        MELEE = 'Melee'
        RANGED = 'RANGED'



    weapon_type = models.CharField(blank=True,
                                   choices=WeaponType.choices,
                                   max_length=10,
                                   default=None)

    item = models.ForeignKey(Weapon, on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             default=None)

    @classmethod
    def create_trait_from_template(cls, trait: Union[WeaponTrait, ArmorTrait, int], item: Union[int, Item], weapon_type, x_value: int=None) -> WeaponTrait:
        new_trait = super()._create_trait_from_template(trait, item, x_value=x_value)

        new_trait.weapon_type = weapon_type

        return new_trait



    def __str__(self):
        return f"{super().__str__()} on {self.item}"