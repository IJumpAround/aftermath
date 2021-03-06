import re
from typing import Optional, Union

from django.db import models, transaction
from django.db.models import Count, Q, ObjectDoesNotExist, Value
from django.core.exceptions import ValidationError
from rest_framework import serializers


class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)

    copper = models.IntegerField(blank=False,
                                 null=False,
                                 default=0)
    silver = models.IntegerField(blank=False,
                                 null=False,
                                 default=0)
    electrum = models.IntegerField(blank=False,
                                   null=False,
                                   default=0)
    gold = models.IntegerField(blank=False,
                               null=False,
                               default=0)
    platinum = models.IntegerField(blank=False,
                                   null=False,
                                   default=0)

    @classmethod
    def get_party(cls):
        return cls.objects.get(name="Party")

    @classmethod
    def get_default(cls):
        party = cls.objects.get_or_create(name="Party", defaults={'name': "Party"})
        return party[0].pk

    def get_owned_items(self):
        items = Item.get_owned_items(self.id)
        return items

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
        verbose_name_plural = 'rarities'

    rarity_level = models.CharField(max_length=40,
                                    unique=True)

    def __str__(self):
        return self.rarity_level


def is_attuned_validator(item):
    if item.is_attuned and (item.player is None or item.player.name == 'Party'):
        raise ValidationError("Must have an owner to be attuned", params={item.is_attuned: 'error'})


class Item(models.Model):

    def clean(self):
        if self.is_attuned and (self.player is None or self.player.name == 'Party'):
            raise ValidationError('Must have an owner to be attuned', params={self.is_attuned: 'Error'})
        super(Item, self).clean()

    class Meta:
        abstract = True

    name = models.CharField(max_length=70)
    text_description = models.TextField()
    flavor = models.TextField(null=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    requires_attunement = models.BooleanField(default=False)
    is_attuned = models.BooleanField(default=False)

    player = models.ForeignKey(Player,
                               on_delete=models.PROTECT,
                               default=Player.get_default,
                               blank=False,
                               null=False,
                               verbose_name='Owner')

    quantity = models.IntegerField(default=1)
    value = models.CharField(default=None, null=True, max_length=30)


    @classmethod
    def query_common_base_fields(cls):
        """To better return a consistent data structure in the main view we retrieve useful properties that
        are common to most items
        """
        query = cls.objects.all().only('id', 'name', 'text_description', 'rarity', 'requires_attunement',
                                       'is_attuned', 'player__name', 'quantity').annotate(
            model_type=Value(cls._meta.verbose_name_plural, output_field=models.CharField())).annotate(
            model_name=Value(cls._meta.model_name, output_field=models.CharField()))
        return query

    @classmethod
    def get_serializer(cls):
        class BaseSerializer(serializers.HyperlinkedModelSerializer):
            player = serializers.StringRelatedField()

            class Meta:
                model = cls
                fields = '__all__'
                depth = 1

        return BaseSerializer

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('item_management:item', kwargs=dict(pk=self.id, item_type=self._meta.model_name))


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

    @transaction.atomic()
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

        if amount > 0:
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

    def name_with_quantity(self):
        return f"{self.name} x {self.quantity}"

    def __str__(self):
        return f"{self.name_with_quantity()} {self.player}"


class Equippable(Item):
    item_slot = models.ForeignKey(ItemSlot,
                                  on_delete=models.DO_NOTHING)
    is_equipped = models.BooleanField(default=False)

    def clean(self):
        if self.is_equipped and not (self.player or self.player == 'Party'):
            raise ValidationError("Cannot be equipped without an owner!", params={self.is_equipped})
        elif not self.requires_attunement and self.is_attuned:
            self.is_attuned = False
            print(self.is_attuned)
        super(Equippable, self).clean()

    class Meta:
        abstract = True


class Armor(Equippable):
    pass

    class Meta:
        verbose_name_plural = "armor"

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


class TraitType(models.TextChoices):
    WEAPON = 'Weapon'
    ARMOR = 'Armor'


class WeaponType(models.TextChoices):
    SPECIAL = 'Special'
    EITHER = 'Either'
    MELEE = 'Melee'
    RANGED = 'Ranged'


class TraitTemplate(models.Model):
    trait_name = models.CharField(max_length=30)
    scaling_trait = models.BooleanField(blank=False,
                                        null=False)
    description = models.TextField()

    tier = models.ForeignKey(Tier,
                             on_delete=models.PROTECT,
                             null=False)

    trait_type = models.CharField(choices=TraitType.choices,
                                  max_length=6,
                                  blank=False,
                                  null=False)

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_trait_type_valid",
                check=models.Q(trait_type__in=TraitType.values),
            )
        ]

    def create_trait_from_template(self, item, **kwargs) -> 'TraitInstanceBase':
        trait = TraitInstanceBase.create_trait_from_template(template=self, item=item, **kwargs)
        return trait

    def __str__(self):
        return self.trait_name


class ArmorTraitTemplate(TraitTemplate):
    trait_type = models.CharField(choices=TraitType.choices,
                                  max_length=6,
                                  blank=False,
                                  null=False,
                                  default=TraitType.ARMOR)
    pass


class WeaponTraitTemplate(TraitTemplate):
    trait_type = models.CharField(choices=TraitType.choices,
                                  max_length=6,
                                  blank=False,
                                  null=False,
                                  default=TraitType.WEAPON)
    weapon_type = models.CharField(blank=False,
                                   choices=WeaponType.choices,
                                   max_length=10,
                                   default=WeaponType.MELEE)


class TraitNameFormatterMixin:
    template: TraitTemplate
    regex: re.Pattern
    x_value: Optional[int]

    def to_string(self):
        template = self.template
        trait_name = template.trait_name
        if template.scaling_trait:
            match = self.regex.search(template.trait_name)
            trait_name = f'{trait_name[:match.start(1)]}{self.x_value}{trait_name[match.end(1):]}'
        return trait_name


class TraitInstanceBase(models.Model, TraitNameFormatterMixin):
    x_value = models.PositiveSmallIntegerField(null=True,
                                               blank=True)
    template: TraitTemplate
    regex = re.compile('\(.*(X).*\)')

    class Meta:
        abstract = True

    def clean(self):
        if not self.template.scaling_trait and self.x_value is not None:
            raise ValidationError('This trait does not scale, please leave x_value blank', {'x_value': self.x_value})
        elif self.template.scaling_trait and self.x_value is None:
            raise ValidationError('This trait scales, please select an x_value', {'x_value': self.x_value})

    @classmethod
    def create_trait_from_template(cls, template: Union[TraitTemplate, int], item: Union[int, Item],
                                   **kwargs) -> 'TraitInstanceBase':
        """
        Creates a trait instance from a template and associates it with the item provided.
        Args:
            template: the template we are copying
            item: the item to apply this trait to
            **kwargs:
                x_level is required if the template is a scaling trait
                weapon_type is required for weapon traits

        Returns: An instance of a WeaponTrait or ArmorTrait

        """
        if isinstance(template, int):
            template = TraitTemplate.objects.get(id=template)

        if isinstance(item, Item):
            item = item.id

        if not template.scaling_trait:
            kwargs['x_value'] = None
        elif template.scaling_trait and not kwargs.get('x_value'):
            raise ValidationError("x_value must be provided for a scaling trait instance")

        if template.trait_type == TraitType.ARMOR:
            clazz = ArmorTrait
        else:
            clazz = WeaponTrait
            kwargs['weapon_type'] = template.weapon_type

        return clazz.objects.create(template=template, item_id=item, **kwargs)


class ArmorTrait(TraitInstanceBase):
    template = models.ForeignKey(ArmorTraitTemplate, on_delete=models.CASCADE)
    item = models.ForeignKey(Armor, on_delete=models.SET_NULL,
                             null=True,
                             blank=False,
                             default=None)

    def __str__(self):
        return f"{super().to_string()} on {self.item}"


class WeaponTrait(TraitInstanceBase):
    template = models.ForeignKey(WeaponTraitTemplate, on_delete=models.CASCADE)

    item = models.ForeignKey(Weapon, on_delete=models.CASCADE,
                             null=True,
                             blank=False,
                             default=None)

    def __str__(self):
        return f"{super().to_string()} on {self.item}"
