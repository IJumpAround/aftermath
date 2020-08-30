from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.utils.log import request_logger

from .serializers import UserSerializer, GroupSerializer, PlayerSerializer, ArmorSerializer, \
    RaritySerializer, ItemSlotSerializer, WeaponSerializer
from .models import *



class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('-name')
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArmorViewSet(viewsets.ModelViewSet):
    queryset = Armor.objects.all()
    serializer_class = ArmorSerializer
    permission_classes = [permissions.IsAuthenticated]


class RarityViewSet(viewsets.ModelViewSet):
    queryset = Rarity.objects.all()
    serializer_class = RaritySerializer
    permission_classes = [permissions.IsAuthenticated]


class ItemSlotViewSet(viewsets.ModelViewSet):
    queryset = ItemSlot.objects.all()
    serializer_class = ItemSlotSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(http_method_names=['GET'])
def get_all_items(request):
    request_logger.info('get_all_items')
    weapons = Weapon.objects.all().select_related()
    armor = Armor.objects.all().select_related()

    armor_serializer = ArmorSerializer(armor, many=True)
    weapon_serialzer = WeaponSerializer(weapons, many=True)
    item_list = {'armor': armor_serializer.data, 'weapons': weapon_serialzer.data}
    return Response(item_list, 200)
