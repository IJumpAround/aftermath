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
        return f"{self.name}"


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
    slot_name = models.CharField(max_length=30)

    def __str__(self):
        return self.slot_name


class Rarity(models.Model):
    rarity_level = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Rarities'

    def __str__(self):
        return self.rarity_level


class Item(models.Model):
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL,
                               null=True)
    wondrous = models.BooleanField(default=False)
    requires_attunement = models.BooleanField(default=False)
    description = models.OneToOneField(Description, on_delete=models.CASCADE)

    player = models.ForeignKey(Player,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)

    class Meta:
        abstract = True


class Equippable(Item):
    item_slot = models.ForeignKey(ItemSlot,
                                  on_delete=models.PROTECT)

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


class Tier(models.Model):
    description = models.CharField(max_length=125)
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

