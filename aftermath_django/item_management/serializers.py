from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Player, Armor, Rarity, Tier, ArmorTrait, WeaponTrait, Weapon, ItemSlot, Item, Stackable


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


# Example of serializer using reverse relation to retrieve "owned" items
class PlayerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Player
        fields = ('name', 'weapon_set', 'armor_set', 'copper', 'silver','electrum','gold','platinum')


class ArmorSerializer(serializers.ModelSerializer):
    # description = PrimaryKeyRelatedField(queryset=Description.objects.all())
    class Meta:
        model = Armor
        fields = '__all__'


class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = '__all__'


class ItemSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSlot
        fields = '__all__'


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        depth = 1
        fields = '__all__'

class StackableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stackable
        depth = 1
        fields = ('id', 'name', 'text_description', 'stackable_type', 'rarity', 'quantity', 'player')
