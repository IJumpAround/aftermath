from django.db import models
from django.core.validators import MaxValueValidator


class Description(models.Model):
    """
    Descriptive elements of an item including its name,
    usage description, and flavor.
    """
    name = models.CharField(max_length=70)
    text_description = models.TextField()
    lore = models.TextField()


class Player(models.Model):
    name = models.CharField(max_length=50)
    attunement_slots = models.PositiveSmallIntegerField(validators=(MaxValueValidator(limit_value=3),))
    # Items
    # Effects


class ItemSlot(models.Model):
    slot_name = models.TextField(30)


class Rarity(models.Model):
    rarity_level = models.CharField(max_length=40)


class Item(models.Model):
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL)
    item_type = models.CharField(max_length=50)  # ring, head, consumable
    wondrous = models.BooleanField(default=False)
    requires_attunement = models.BooleanField(default=False)
    description = models.ForeignKey(Description, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Equippable(Item):
    item_slot = models.ForeignKey(ItemSlot,
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True)
    player = models.ForeignKey(Player,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)

    class Meta:
        abstract = True


class Weapon(Equippable):
    damage = models.TextField(35)
    range = models.TextField(30, default=None)
    # Weapon mod


class Trait(models.Model):
    trait_name = models.CharField(30)
    trait_level = models.PositiveSmallIntegerField(null=True,
                                                   blank=True)
    description = models.CharField(140)

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
                                   max_length=1,
                                   default=None)


class Tier(models.Model):
    description = models.CharField(max_length=125)
    level = models.SmallIntegerField()
    trait = models.ForeignKey(Trait, on_delete=models.DO_NOTHING)
