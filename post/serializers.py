from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PostSerializer(serializers.ModelSerializer):

    writer = UserSerializer()

    class Meta:

        model = Post
        fields = ('title', 'text', 'date', 'writer')
