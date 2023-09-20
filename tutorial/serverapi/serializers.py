from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.db import models
from django.urls import reverse

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta (object):
        model = User
        fields = ['id', 'username', 'email', 'password',]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class openAISerializer(serializers.Serializer):
   prompt = serializers.CharField()




class Book(models.Model):
    name = models.CharField(max_length=200)
    pages = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book_edit', kwargs={'pk': self.pk})