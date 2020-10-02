from typing import Optional

from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Count, Q, ObjectDoesNotExist
from rest_framework import serializers


class Player(models.Model):
    name = models.CharField(max_length=50)
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


    def get_items(self):
        armor = Armor.objects.filter(player_id=self.id)
        return armor

    def __str__(self):
        return self.name
    # Items
    # Effects


class ItemSlot(models.Model):
    class SlotTypeChoices(models.TextChoices):
        WEAPON = 'Weapon'
        ARMOR = 'Armor'
        ACCESSORY = 'Accessory'

    slot_name = models.CharField(max_length=30)
    slot_type = models.TextField(choices=SlotTypeChoices.choices)

    def __str__(self):
        return self.slot_name


class Rarity(models.Model):
    rarity_level = models.CharField(max_length=40,
                                    unique=True)

    class Meta:
        verbose_name_plural = 'Rarities'

    def __str__(self):
        return self.rarity_level


class Item(models.Model):
    name = models.CharField(max_length=70)
    text_description = models.TextField()
    flavor = models.TextField(null=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    wondrous = models.BooleanField(default=False)
    requires_attunement = models.BooleanField(default=False)

    player = models.ForeignKey(Player,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)


    class Meta:
        abstract = True

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
        item = Stackable.objects.get(Q(player__name=None) | Q(player__name="Party"))
        count = item.quantity
        return count

    def transfer_to_party(self, amount):
        return self._transfer(player=None, amount=amount)

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
            except ObjectDoesNotExist as e:
                target_stack = Stackable.objects.create(player_id=new_owner_id)

            target_stack.quantity += actual_amount
            target_stack.save()
            target_stack.refresh_from_db()
            return target_stack


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
    trait_level = models.PositiveSmallIntegerField(null=True,
                                                   blank=True)
    description = models.CharField(max_length=140)
    item = models.ForeignKey(Armor, on_delete=models.SET_NULL,
                             null=True,
                             default=None)
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT,
                             null=False,
                             default=0)

    class Meta:
        abstract = True


class ArmorTrait(Trait):
    pass


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
