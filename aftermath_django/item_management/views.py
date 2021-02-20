from functools import reduce

from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from django.utils.log import request_logger

from .serializers import (UserSerializer, GroupSerializer, PlayerSerializer, ArmorSerializer,
                          RaritySerializer, ItemSlotSerializer, WeaponSerializer, StackableSerializer,
                          WeaponTraitSerializer, BaseItemSerializer)
from .models import *


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('-name')
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'

    @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated],
            url_path='items', url_name='items')
    def get_items(self, request, pk=None):
        player = self.get_object()

        return player.get_owned_items()


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


class WeaponViewSet(viewsets.ModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer
    permission_classes = [permissions.IsAuthenticated]


class StackableViewSet(viewsets.ModelViewSet):
    queryset = Stackable.objects.all()
    serializer_class = StackableSerializer
    permission_classes = [permissions.IsAuthenticated]


class WeaponTraitViewSet(viewsets.ModelViewSet):
    queryset = WeaponTrait.objects.all()
    serializer_class = WeaponTraitSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArmorTraitViewSet(viewsets.ModelViewSet):
    queryset = ArmorTrait.objects.all()
    serializer_class = WeaponTraitSerializer
    permission_classes = [permissions.IsAuthenticated]


class ViewPaginatorMixin(object):
    min_limit = 1
    max_limit = 10

    def paginate(self, object_list, page=1, limit=10, **kwargs):
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (TypeError, ValueError):
            page = 1

        try:
            limit = int(limit)
            if limit < self.min_limit:
                limit = self.min_limit
            if limit > self.max_limit:
                limit = self.max_limit
        except (ValueError, TypeError):
            limit = self.max_limit

        paginator = Paginator(object_list, limit)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        data = {
            'previous_page': objects.has_previous() and objects.previous_page_number() or None,
            'next_page': objects.has_next() and objects.next_page_number() or None,
            'data': list(objects),
            'count': len(objects),
            'total_items': len(object_list)
        }
        return data


class MainItemsView(ViewPaginatorMixin, viewsets.ViewSet):

    def post(self, request: Request):
        request_logger.info('get_all_items')
        request_logger.info(request.data)

        body = request.data

        limit = int(body.get('length', 25))
        page = int(body.get('start', 1)) // int(limit)
        order_by = body.get('order')

        search_term = body.get('search', {}).get('value')

        querysets = [Weapon.query_common_base_fields(), (Armor.query_common_base_fields()),
                     Stackable.query_common_base_fields()]

        if search_term and len(search_term) >= 1:
            querysets = list(map(lambda query: query.filter(Q(name__icontains=search_term) |
                                                            Q(player__name__icontains=search_term)), querysets))

        queryset = reduce(lambda x, y: x.union(y), querysets)

        if order_by:
            order_by = order_by[0]
            order_col = body.get('columns')[order_by['column']]
            direction = '' if order_by['dir'] == 'asc' else '-'
            order_by = direction + order_col['data']
        else:
            order_by = 'name'

        queryset = queryset.order_by(order_by)

        items = BaseItemSerializer(queryset, many=True, context={'request': request}).data
        return Response({"resources": self.paginate(items, page, limit)})

    def get(self, request: Request):
        request_logger.info('get_all_items')

        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 25)
        order_by = request.query_params.get('order_by', 'name')
        queryset = Weapon.query_common_base_fields().union(Armor.query_common_base_fields()).union(
            Stackable.query_common_base_fields()).order_by(order_by)

        items = BaseItemSerializer(queryset, many=True, context={'request': request}).data
        return Response({"resources": self.paginate(items, page, limit)})
