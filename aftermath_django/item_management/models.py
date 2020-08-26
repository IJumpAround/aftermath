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

    def __str__(self):
        return f"{self.name}\n" \
               f"**{self.lore}**\n" \
               f"{self.text_description}"


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
    slot_name = models.TextField(30)


class Rarity(models.Model):
    rarity_level = models.CharField(max_length=40)

    def __str__(self):
        return self.rarity_level


class Item(models.Model):
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL,
                               null=True)
    item_type = models.CharField(max_length=50)  # ring, head, consumable
    wondrous = models.BooleanField(default=False)
    requires_attunement = models.BooleanField(default=False)
    description = models.ForeignKey(Description, on_delete=models.CASCADE)

    player = models.ForeignKey(Player,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)

    class Meta:
        abstract = True


class Equippable(Item):
    item_slot = models.ForeignKey(ItemSlot,
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True)

    class Meta:
        abstract = True


class Armor(Equippable):
    pass

    class Meta:
        verbose_name_plural = "Armor"

    def __str__(self):
        return self.description.name

class Weapon(Equippable):
    damage = models.TextField(35)
    range = models.TextField(30, default=None)
    # Weapon mod


class Trait(models.Model):
    trait_name = models.CharField(max_length=30)
    trait_level = models.PositiveSmallIntegerField(null=True,
                                                   blank=True)
    description = models.CharField(max_length=140)
    item = models.ForeignKey(Armor, on_delete=models.SET_NULL,
                             null=True,
                             default=None)

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


class Tier(models.Model):
    description = models.CharField(max_length=125)
    level = models.SmallIntegerField()
    weapon_trait = models.ForeignKey(WeaponTrait, on_delete=models.DO_NOTHING,
                                     null=True,
                                     default=True)
    armor_trait = models.ForeignKey(ArmorTrait, on_delete=models.DO_NOTHING,
                                    null=True,
                                    default=None)
