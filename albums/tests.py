from rest_framework.test import APITestCase
from rest_framework import status
from . import models

class BaseTest(APITestCase):
    def setUp(self) -> None:
        self.artist = models.Artist.objects.create(name="test artist")
        self.album = models.Album.objects.create(artist=self.artist, year=2000)
        self.song = models.Song.objects.create(album=self.album, title="test song")

class TestCreate(BaseTest):
    def check_create(self, url: str, model, text: dict, status, count: int) -> None:
        response = self.client.post(url, text, format='json')
        self.assertEqual(response.status_code, status)
        self.assertEqual(model.objects.count(), count)
        self.assertEqual(model.objects.filter(id=2).count(), count - 1)

    def test_main_create(self) -> None:
        self.check_create('/api/artists/', models.Artist, {'name': 'test artist'}, status.HTTP_201_CREATED, 2)
        self.check_create('/api/albums/', models.Album, {'artist': self.artist.id, 'year': 2001}, status.HTTP_201_CREATED, 2)
        self.check_create('/api/songs/', models.Song, {'album': self.album.id, 'title': 'test song'}, status.HTTP_201_CREATED, 2)

        
    def test_main_create_null(self) -> None:
        self.check_create('/api/artists/', models.Artist, {'name': ''}, status.HTTP_400_BAD_REQUEST, 1)
        self.check_create('/api/albums/', models.Album, {'artist': self.artist.id, 'year': 1000}, status.HTTP_400_BAD_REQUEST, 1)
        self.check_create('/api/songs/', models.Song, {'album': self.album.id, 'title': ''}, status.HTTP_400_BAD_REQUEST, 1)

    def test_main_create_long(self) -> None:
        self.check_create('/api/artists/', models.Artist, {'name': 'a' * 65}, status.HTTP_400_BAD_REQUEST, 1)
        self.check_create('/api/albums/', models.Album, {'artist': self.artist.id, 'year': 2031}, status.HTTP_400_BAD_REQUEST, 1)
        self.check_create('/api/songs/', models.Song, {'album': self.album.id, 'title': 'a' * 65}, status.HTTP_400_BAD_REQUEST, 1)

    def test_main_create_short(self) -> None:
        self.check_create('/api/artists/', models.Artist, {'name': 'a'}, status.HTTP_400_BAD_REQUEST, 1)
        self.check_create('/api/albums/', models.Album, {'artist': self.artist.id, 'year': 1899}, status.HTTP_400_BAD_REQUEST, 1)
        self.check_create('/api/songs/', models.Song, {'album': self.album.id, 'title': 'a'}, status.HTTP_400_BAD_REQUEST, 1)

class TestGet(BaseTest):
    def check_get(self, url: str, model, status) -> None:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status)

    def test_main_get(self) -> None:
        self.check_get(f'/api/artists/{self.artist.id}/', models.Artist, status.HTTP_200_OK)
        self.check_get(f'/api/albums/{self.album.id}/', models.Album, status.HTTP_200_OK)
        self.check_get(f'/api/songs/{self.song.id}/', models.Song, status.HTTP_200_OK)

    def test_main_get_null(self) -> None:
        self.check_get(f'/api/artists/{self.artist.id + 1}/', models.Artist, status.HTTP_404_NOT_FOUND)
        self.check_get(f'/api/albums/{self.album.id + 1}/', models.Album, status.HTTP_404_NOT_FOUND)
        self.check_get(f'/api/songs/{self.song.id + 1}/', models.Song, status.HTTP_404_NOT_FOUND)

    def test_main_get_all(self) -> None:
        self.check_get(f'/api/artists/', models.Artist, status.HTTP_200_OK)
        self.check_get(f'/api/albums/', models.Album, status.HTTP_200_OK)
        self.check_get(f'/api/songs/', models.Song, status.HTTP_200_OK)

class TestDelete(BaseTest):
    def check_delete(self, url: str, model, status, count: int) -> None:
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status)
        self.assertEqual(model.objects.count(), count)

    def test_main_delete(self) -> None:
        self.check_delete(f'/api/songs/{self.song.id}/', models.Song, status.HTTP_204_NO_CONTENT, 0)
        self.check_delete(f'/api/albums/{self.album.id}/', models.Album, status.HTTP_204_NO_CONTENT, 0)
        self.check_delete(f'/api/artists/{self.artist.id}/', models.Artist, status.HTTP_204_NO_CONTENT, 0)