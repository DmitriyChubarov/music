from django.shortcuts import render
from django.db.models import QuerySet

from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .repositories import BaseRepository

from .models import Artist, Album, Song

from .serializers import SongSerializer, AlbumSerializer, AlbumDetailSerializer, ArtistSerializer, ArtistDetailSerializer

class ArtistViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    def get_queryset(self) -> QuerySet:
        return BaseRepository.get_objects(Artist)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        return ArtistSerializer


class AlbumViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    def get_queryset(self) -> QuerySet:
        return BaseRepository.get_objects(Album)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlbumDetailSerializer
        return AlbumSerializer


class SongViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    def get_queryset(self) -> QuerySet:
        return BaseRepository.get_objects(Song)
    serializer_class = SongSerializer