from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
# import datetime

# Create your models here.


class Post(models.Model):
    '''
    Model for keeping posts on database
    '''
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    text = models.CharField(max_length=1000, blank=False, null=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    # date = models.DateTimeField(default=datetime.datetime.now, blank=False)

    def __str__(self):
        return '"' + self.title + '"' + ' by ' + self.writer.username
