from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Count, Q, F
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


    def split(self, player_name, amount):
        new_owner = Player.objects.filter(name__exact=player_name)

        if self.quantity > amount > 0 and new_owner:
            self.quantity = F('quantity') - amount
            self.save()
            self.refresh_from_db()

            new_stack = Stackable.objects.get(pk=self.id)
            new_stack.id = None
            new_stack.quantity = amount
            new_stack.save()
            return new_stack


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
