# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
import uuid


class Album(models.Model):
    album_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    photo_link = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'album'


class Comments(models.Model):
    c_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    song = models.ForeignKey('Song', models.DO_NOTHING, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comments'

    def __str__(self):
        return f'Comment by {self.user} on {self.song.name}'


class Playlist(models.Model):
    list_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    photo_link = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'playlist'


class Singer(models.Model):
    singer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    photo_link = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'singer'


class Song(models.Model):
    song_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    photo_link = models.CharField(max_length=100, blank=True, null=True)
    lyric = models.CharField(max_length=10000, blank=True, null=True)
    audio_link = models.CharField(max_length=100, blank=True, null=True)
    singer = models.ForeignKey(Singer, models.DO_NOTHING, blank=True, null=True)
    album = models.ForeignKey(Album, models.DO_NOTHING, blank=True, null=True)
    style = models.ForeignKey('Style', models.DO_NOTHING, blank=True, null=True)
    playlist=models.ManyToManyField(Playlist,through='Have')
    #favouritelist=models.ManyToManyField('FavouriteList',through='Exist',through_fields=('song','user_id','list_id'))


    class Meta:
        managed = True
        db_table = 'song'


class Style(models.Model):
    style_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'style'


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    e_mail = models.CharField(max_length=80, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'

class FavouriteList(models.Model):
    list_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100,blank=True,null=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        managed=True
        db_table='favourite_list'
        ordering=['list_id']
        unique_together = (('list_id', 'user_id'),)

class Have(models.Model):
    song = models.ForeignKey('Song', models.DO_NOTHING, primary_key=True)  # The composite primary key (song_id, playlist_id) found, that is not supported. The first column is selected.
    playlist = models.ForeignKey('Playlist', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'have'
        unique_together = (('song', 'playlist'),)

class Exist(models.Model):
    list=models.ForeignKey(FavouriteList,related_name="list_song",on_delete=models.CASCADE,primary_key=True)
    user = models.ForeignKey(FavouriteList, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'exist'
        unique_together = (('list_id', 'user_id','song_id'),)


