from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import filters

from api.mixins import UltraModelViewSet
from api.filters import RepertoireFilter, PerformanceSeanceFilter
from api.paginations import SimpleResultPagination
from api.serializers import (NewsSerializer, PhotoSerializer, PhotoCategorySerializer, EventSerializer,
                             HallSerializer, RepertoireSerializer, CartSerializer, CartTicketSerializer,
                             CreateCartSerializer, PerformanceSeanceSerializer)
from core.models import *
from cart.models import *


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = NewsSerializer
    lookup_field = 'id'
    search_fields = ['title', 'description', 'content']


class PhotoViewSet(ReadOnlyModelViewSet):
    queryset = Photo.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = PhotoSerializer
    lookup_field = 'id'
    search_fields = ['photo_cat', 'created_at',]


class PhotoCategoryViewSet(ReadOnlyModelViewSet):
    queryset = PhotoCategory.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = PhotoCategorySerializer
    lookup_field = 'id'
    search_fields = ['name', 'created_at',]


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = EventSerializer
    lookup_field = 'id'
    search_fields = ['name', 'created_at',]


class HallViewSet(ReadOnlyModelViewSet):
    queryset = Hall.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = HallSerializer
    lookup_field = 'id'
    search_fields = ['name', 'created_at',]


class PerformanceSeanceViewSet(ReadOnlyModelViewSet):
    queryset = PerformanceSeance.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = PerformanceSeanceSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['id', 'created_at', 'date', 'time']
    filterset_class = PerformanceSeanceFilter


class RepertoireViewSet(ReadOnlyModelViewSet):
    queryset = Repertoire.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = RepertoireSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'created_at', 'date']
    filterset_class = RepertoireFilter
    ordering_fields = ['pg',]


class CartViewSet(UltraModelViewSet):
    queryset = Cart.objects.all()
    serializer_classes = {
        'list': CartSerializer,
        'retrieve': CartSerializer,
        'update': CartSerializer,
        'create': CreateCartSerializer,
    }
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    search_fields = ['name', 'email', 'phone', 'date_of_birth']
    filterset_fields = ['tickets__ticket']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (AllowAny,),
        'update': (IsAuthenticated,),
        'destroy': (IsAuthenticated,),
    }


class CartTicketViewSet(ModelViewSet):
    queryset = TicketForSale.objects.all()
    serializer_class = CartTicketSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['price',]
    filterset_fields = ['ticket', 'cart']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (AllowAny,),
        'update': (IsAuthenticated,),
        'destroy': (IsAuthenticated,),
    }

