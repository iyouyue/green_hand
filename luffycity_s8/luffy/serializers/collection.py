from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from luffy import models



class CollectionSerializer(ModelSerializer):
    class Meta:
        model = models.Collection
        fields = "__all__"


class CollectionDetailSerializer(ModelSerializer):
    class Meta:
        model = models.Collection
        fields = "__all__"


