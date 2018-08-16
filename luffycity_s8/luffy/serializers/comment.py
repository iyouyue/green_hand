from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from luffy import models



class CommentSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class CommentDetailSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


