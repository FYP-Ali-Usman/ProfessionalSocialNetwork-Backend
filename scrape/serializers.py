from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.Serializer):
    # class Meta:
    #     model = Movie
    #     fields = ('title', 'year')
    # year = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    url = serializers.CharField(required=True, allow_blank=False)
    name = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return URL.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.url = validated_data.get('title', instance.url)
        instance.name = validated_data.get('year', instance.name)
        instance.save()
        return instance