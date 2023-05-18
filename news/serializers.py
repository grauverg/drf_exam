from django.db import IntegrityError
from rest_framework import serializers

from . import models


class NewsSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = models.News
        fields = '__all__'
        read_only_field = ['author', ]


class CommentSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = models.Comment
        fields = '__all__'
        read_only_field = ['author', ]


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            return {"error": "You already added status"}


class NewsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsStatus
        fields = '__all__'
        read_only_fields = ['author', 'news']


class CommentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentStatus
        fields = '__all__'
        read_only_fields = ['author', 'comment']
