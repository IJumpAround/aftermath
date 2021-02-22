from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import (Player, Armor, Rarity, ArmorTrait, WeaponTrait, Weapon, ItemSlot, Stackable,
                     WeaponTraitTemplate, ArmorTraitTemplate)


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
        fields = ('id', 'name', 'weapon_set', 'armor_set', 'copper', 'silver', 'electrum', 'gold', 'platinum')


class SimplePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('name')


class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = '__all__'


class ItemSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSlot
        fields = '__all__'


class StackableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stackable
        depth = 1
        fields = ('id', 'name', 'text_description', 'stackable_type', 'rarity', 'quantity', 'player')


class ArmorTraitTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArmorTraitTemplate
        fields = '__all__'


class WeaponTraitTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponTraitTemplate
        fields = '__all__'


class ArmorTraitSerializer(serializers.ModelSerializer):
    template = ArmorTraitTemplateSerializer()

    class Meta:
        model = ArmorTrait
        fields = '__all__'


class WeaponTraitSerializer(serializers.ModelSerializer):
    template = WeaponTraitTemplateSerializer()

    class Meta:
        model = WeaponTrait
        fields = '__all__'


class ArmorSerializer(serializers.ModelSerializer):
    armortrait_set = ArmorTraitSerializer(many=True, read_only=True)

    class Meta:
        model = Armor
        fields = '__all__'


class WeaponSerializer(serializers.ModelSerializer):
    weapontrait_set = WeaponTraitSerializer(many=True, read_only=True)

    class Meta:
        model = Weapon
        fields = '__all__'


class ModelNameField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return value._meta.model_name


class BaseItemSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    model_type = serializers.CharField()
    name = serializers.CharField()
    text_description = serializers.CharField()
    rarity = RaritySerializer()
    requires_attunement = serializers.BooleanField()
    player = serializers.StringRelatedField()
    quantity = serializers.IntegerField()
    model_name = serializers.CharField()
    is_attuned = serializers.BooleanField()
