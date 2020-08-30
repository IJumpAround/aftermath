from django.db import models
from django.core.validators import MaxValueValidator

class Player(models.Model):
    name = models.CharField(max_length=50)
    attunement_slots = models.PositiveSmallIntegerField(validators=(MaxValueValidator(limit_value=3),),
                                                        default=3,
                                                        blank=True)

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

# Hold fields from different models which will be returned as a list of one object type
class GenericItem(models.Model):

    class Meta:
        abstract = True
        managed = False

