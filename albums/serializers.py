from rest_framework import serializers

from .models import Artist, Album, Song

'''Главные сериализаторы'''
class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']   
        
class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.name', read_only=True)

    class Meta:
        model = Album
        fields: list[str] = ['id', 'artist', 'artist_name', 'year']   

class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='album.artist.name', read_only=True)

    class Meta:
        model = Song
        fields: list[str] = ['id', 'album', 'title', 'artist_name', 'track_number']  

'''Точечные сериализаторы'''
class SongDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'track_number']

class AlbumDetailSerializer(serializers.ModelSerializer):
    songs = SongDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'year', 'artist', 'songs']

class ArtistDetailSerializer(serializers.ModelSerializer):
    albums = AlbumDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ['id', 'name', 'albums']

        
        
        





