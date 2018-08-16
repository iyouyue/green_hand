from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from luffy import models



class ArticleSerializer(ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['id', 'title','brief','date','comment_num','agree_num','view_num','collect_num','head_img']


class ArticleDetailSerializer(ModelSerializer):
    class Meta:
        model = models.Article
        exclude = ["brief",'article_type','status','order','vid','position','source','pub_date','offline_date']
        depth=2

    comments = serializers.SerializerMethodField()
    collectors = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comment_list = models.Comment.objects.filter(object_id=obj.id)
        return [{'user': row.account.username, 'content': row.content} for row in comment_list]

    def get_collectors(self, obj):
        collector_list = models.Collection.objects.filter(object_id=obj.id)
        return [{'user': row.account.username, 'content': row.date} for row in collector_list]

