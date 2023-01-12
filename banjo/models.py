from django.db import models
from django.conf import settings


# Create your models here.
class Songs(models.Model):
    title = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255, null=False)
    song = models.FileField(upload_to='' , null=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)
    album = models.ImageField(upload_to ='album/',null=True)
    
    def __str__(self):
        return "{} - {} - {} - {}- {}-{}".format(self.id, self.title, self.artist, self.song , self.uploader ,self.album)