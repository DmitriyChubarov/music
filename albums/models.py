from django.db import models, transaction
from django.db.models import Max
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator

class Artist(models.Model):
    name = models.CharField(max_length=64, validators=[MinLengthValidator(3), MaxLengthValidator(64)])

    def __str__(self):
        return self.name

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2030)])

    class Meta:
        ordering = ['year']

    def __str__(self):
        return f"{self.artist.name} - {self.year}"


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', verbose_name='Альбом')
    title = models.CharField(max_length=64, verbose_name='Название', validators=[MinLengthValidator(3), MaxLengthValidator(64)])
    track_number = models.PositiveIntegerField(editable=False, verbose_name='Порядковый номер в альбоме')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['album', 'track_number'], name='unique_track_per_album')
        ]
        ordering = ['track_number']

    def __str__(self):
        return f"{self.track_number}. {self.title}"

    def save(self, *args, **kwargs):
        if self.track_number is None and self.album_id is not None:
            with transaction.atomic():
                last_number = (
                    Song.objects
                    .filter(album=self.album)
                    .aggregate(max_num=Max('track_number'))['max_num']
                    or 0
                )
                self.track_number = last_number + 1
        super().save(*args, **kwargs)