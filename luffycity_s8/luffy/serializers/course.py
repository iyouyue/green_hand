from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from luffy import models


class DegreeCourseSerializer(ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = ['id', 'name']


class CourseSerializer(ModelSerializer):
    category = serializers.CharField(source='sub_category.name')
    class Meta:
        model = models.Course
        fields = ['id', 'name','category',]


class DegreeCourseDetailSerializer(ModelSerializer):
    show_teachers = serializers.SerializerMethodField()
    price_policy = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ['id', 'name', 'show_teachers', 'price_policy', 'brief', 'prerequisite', 'period']

    def get_show_teachers(self, obj):
        teacher_list = obj.teachers.all()
        return [{'id': row.id, 'name': row.name} for row in teacher_list]

    def get_price_policy(self, obj):
        price_policy_list = obj.degreecourse_price_policy.all()
        return [{'id': row.id, 'price': row.price, 'period': row.get_valid_period_display()} for row in
                price_policy_list]


class CourseDetailSerializer(ModelSerializer):
    show_teachers = serializers.SerializerMethodField()
    price_policy = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    chapters = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    gaishu = serializers.SerializerMethodField()
    tuijian = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = "__all__"
        # depth = 2

    def get_show_teachers(self, obj):
        teacher_list = obj.coursedetail.teachers.all()
        return [{'id': row.id, 'name': row.name} for row in teacher_list]

    def get_comments(self, obj):
        comment_list = models.Comment.objects.filter(object_id=obj.id)
        return [{'id': row.id, 'content': row.content,'user':row.account.username} for row in comment_list]

    def get_gaishu(self, obj):
        course_gaishu = obj.coursedetail.video_brief_link
        return course_gaishu

    def get_tuijian(self, obj):
        course_tuijian = obj.coursedetail.recommend_courses.all()
        return [{'id': row.id, 'name': row.name} for row in course_tuijian]



    def get_questions(self, obj):
        question_list = models.OftenAskedQuestion.objects.filter(object_id=obj.id)
        print(question_list)
        return [{'id': row.id, 'question': row.question,'answer':row.answer} for row in question_list]

    def get_chapters(self, obj):
        chapter_list = models.CourseChapter.objects.filter(course_id=obj.id)
        return [{'id': row.chapter, 'name': row.name} for row in chapter_list]

    def get_price_policy(self, obj):
        price_policy_list = obj.price_policy.all()
        return [{'id': row.id, 'price': row.price, 'period': row.get_valid_period_display()} for row in
                price_policy_list]

