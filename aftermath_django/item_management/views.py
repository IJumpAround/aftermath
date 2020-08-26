from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, PlayerSerializer, ArmorSerializer, DescriptionSerializer
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
    permission_classes = [permissions.IsAuthenticated]


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


class DescriptionViewSet(viewsets.ModelViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]