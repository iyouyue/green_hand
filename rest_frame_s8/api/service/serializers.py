
from rest_framework import serializers
from ..models import *

class BookSerializers(serializers.ModelSerializer):
    # publish=serializers.HyperlinkedIdentityField(
    #     view_name="publish_detail",
    #     lookup_field="publish_id",
    #     lookup_url_kwarg="pk"
    #     # publishes/(?P<pk>\d+)/$
    # )
    class Meta:
        model=Book
        fields="__all__"

    authors = serializers.SerializerMethodField()
    def get_authors(self,obj):
        temp=[]
        for author in obj.authors.all():
            temp.append({"pk":author.pk,"name":author.name})
        return temp

class PublishSerializers(serializers.ModelSerializer):
    class Meta:
        model=Publish
        fields="__all__"


