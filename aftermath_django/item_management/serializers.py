from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Player, Armor, Description


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
        fields = ('name', 'weapon_set', 'armor_set')


class ArmorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Armor
        fields = '__all__'


class DescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'
