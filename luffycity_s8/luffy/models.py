from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import hashlib
import datetime


# ############ 1. 课程相关 #############
class CourseCategory(models.Model):
    """课程大类, e.g 前端  后端..."""
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "课程大类"
        verbose_name_plural = "课程大类"


class CourseSubCategory(models.Model):
    """课程子类, e.g python linux """
    category = models.ForeignKey("CourseCategory")
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "课程子类"
        verbose_name_plural = "课程子类"


class DegreeCourse(models.Model):
    """学位课程"""
    name = models.CharField(max_length=128, unique=True)
    course_img = models.CharField(max_length=255, verbose_name="缩略图")
    brief = models.TextField(verbose_name="学位课程简介", )
    total_scholarship = models.PositiveIntegerField(verbose_name="总奖学金(贝里)", default=40000)
    mentor_compensation_bonus = models.PositiveIntegerField(verbose_name="本课程的导师辅导费用(贝里)", default=15000)
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=150, help_text='为了计算学位奖学金')
    prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")

    # 用于GenericForeignKey反向查询， 不会生成表字段，切勿删除
    # coupon = GenericRelation("Coupon")
    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    degreecourse_price_policy = GenericRelation("PricePolicy")

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """讲师、导师表"""
    name = models.CharField(max_length=32, verbose_name='姓名')
    role_choices = ((1, '讲师'), (2, '导师'))
    role = models.SmallIntegerField(choices=role_choices, default=1)

    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", blank=True, null=True)
    image = models.CharField(max_length=128, verbose_name='头像')
    brief = models.TextField(max_length=1024, verbose_name='简介')

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    """学位课程奖学金，例如：使用20%的时间学完课程，则奖励5000；使用50%的时间学完课程，则奖励2000"""
    degree_course = models.ForeignKey("DegreeCourse")
    time_percent = models.PositiveSmallIntegerField(verbose_name="奖励档位(时间百分比)", help_text="只填百分值，如80,代表80%")
    value = models.PositiveIntegerField(verbose_name="奖学金数额")


class Course(models.Model):
    """普通课程或学位课的模块"""
    name = models.CharField(max_length=128, unique=True, verbose_name='课程名称或学位课模块名称')
    course_img = models.CharField(max_length=255, verbose_name='课程图片')
    sub_category = models.ForeignKey("CourseSubCategory", verbose_name='课程所属类')

    course_type_choices = ((1, '付费'), (2, 'VIP专享'), (3, '学位课程'))
    course_type = models.SmallIntegerField(choices=course_type_choices)

    # 和学位课做FK，可以为  blank=True, null=True,
    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, help_text="若是学位课程的模块，此处关联学位表")


    brief = models.TextField(verbose_name="课程概述", max_length=2048)
    level_choices = ((1, '初级'), (2, '中级'), (3, '高级'))
    level = models.SmallIntegerField(choices=level_choices, default=1)
    pub_date = models.DateField(verbose_name="发布日期", blank=True, null=True)
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=7)
    order = models.IntegerField("课程顺序", help_text="从上一个课程数字往后排")
    attachment_path = models.CharField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status_choices = ((1, '上线'), (2, '下线'), (3, '预上线'))
    status = models.SmallIntegerField(choices=status_choices, default=1)

    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    # coupon = GenericRelation("Coupon")
    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    price_policy = GenericRelation("PricePolicy")

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.course_type == 3:
            if not self.degree_course:
                raise ValueError("学位课程必须关联对应的学位表")
        super(Course, self).save(*args, **kwargs)


class CourseDetail(models.Model):
    """课程详情页内容"""
    course = models.OneToOneField("Course")
    hours = models.IntegerField("课时")
    course_slogan = models.CharField(max_length=125, blank=True, null=True, verbose_name='课程Slogan')
    video_brief_link = models.CharField(verbose_name='课程介绍', max_length=255, blank=True, null=True)
    why_study = models.TextField(verbose_name="为什么学习这门课程")
    what_to_study_brief = models.TextField(verbose_name="我将学到哪些内容")
    career_improvement = models.TextField(verbose_name="此项目如何有助于我的职业生涯")
    prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")
    recommend_courses = models.ManyToManyField('Course', verbose_name="推荐课程", related_name="recommend_by")

    def __str__(self):
        return self.course.name

class OftenAskedQuestion(models.Model):
    """课程和学位课的常见问题"""

    content_type = models.ForeignKey(ContentType, verbose_name='关联课程或学位课程表')
    object_id = models.PositiveIntegerField(verbose_name='关联课程或学位课程表中的课程ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    question = models.CharField(max_length=255, verbose_name='问题')
    answer = models.TextField(max_length=1024, verbose_name='回答')

    class Meta:
        unique_together = ('content_type', 'object_id', 'question')


class CourseOutline(models.Model):
    """课程大纲"""
    course_detail = models.ForeignKey("CourseDetail")
    title = models.CharField(max_length=128, verbose_name='大纲标题')
    content = models.TextField(max_length=1024, verbose_name='大纲内容')
    order = models.PositiveSmallIntegerField(default=1, verbose_name='大纲显示顺序')

    def __str__(self):
        return self.course_detail.course.name

    class Meta:
        unique_together = ('course_detail', 'title')


class CourseChapter(models.Model):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='course_chapters')
    chapter = models.SmallIntegerField(verbose_name="章节序号（第N章）", default=1)
    name = models.CharField(max_length=128, verbose_name='章节名称')
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    def __str__(self):
        return self.course.name

    class Meta:
        unique_together = ("course", 'chapter')


class CourseSection(models.Model):
    """课时"""
    chapter = models.ForeignKey("CourseChapter", related_name='course_sections')
    name = models.CharField(max_length=128, verbose_name='课程名称')
    section_type_choices = ((1, '文档'), (2, '练习'), (3, '视频'))
    section_type = models.SmallIntegerField(default=3, choices=section_type_choices, verbose_name='课程类型')

    order = models.PositiveSmallIntegerField(verbose_name="课时顺序", help_text="建议每个课时之间空1至2个值，以备后续插入课时")
    section_link = models.CharField(verbose_name='课时链接', max_length=255, blank=True, null=True,
                                    help_text="若是video，填CC视频的唯一标识（如：ECC9954677D8E1079C33DC5901307461）,若是文档或练习，填链接")
    video_time = models.CharField(verbose_name="视频时长(在前端显示)", blank=True, null=True, max_length=32)
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField("是否可试看", default=False)

    class Meta:
        unique_together = ('chapter', 'section_link')


class Homework(models.Model):
    """课程章节作业和考核"""
    chapter = models.ForeignKey("CourseChapter")
    title = models.CharField(max_length=128, verbose_name="作业题目")
    order = models.PositiveSmallIntegerField("作业顺序", help_text="同一课程的每个作业之前的order值间隔1-2个数")
    homework_type_choices = ((1, '作业'), (2, '模块通关考核'))
    homework_type = models.SmallIntegerField(choices=homework_type_choices, default=1)
    requirement = models.TextField(max_length=1024, verbose_name="作业需求")
    threshold = models.TextField(max_length=1024, verbose_name="踩分点")
    recommend_period = models.PositiveSmallIntegerField("推荐完成周期(天)", default=7, help_text='用于计算奖学金')
    scholarship_value = models.PositiveSmallIntegerField("为该作业分配的奖学金(贝里)")
    enabled = models.BooleanField(default=True, help_text="本作业如果后期不需要了，不想让学员看到，可以设置为False")
    note = models.TextField(blank=True, null=True, verbose_name='注意事项')

    class Meta:
        unique_together = ("chapter", "title")


class PricePolicy(models.Model):
    """价格与有课程效期表"""
    content_type = models.ForeignKey(ContentType, verbose_name='关联普通课或者学位课表')
    object_id = models.PositiveIntegerField(verbose_name='关联普通课或者学位课中的课程ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    valid_period_choices = (
        (1, '1天'),
        (3, '3天'),
        (7, '1周'),
        (14, '2周'),
        (30, '1个月'),
        (60, '2个月'),
        (90, '3个月'),
        (180, '6个月'),
        (210, '12个月'),
        (540, '18个月'),
        (720, '24个月'),
    )
    valid_period = models.SmallIntegerField(choices=valid_period_choices, verbose_name='课程周期')
    price = models.FloatField(verbose_name='价格')

    class Meta:
        unique_together = ("content_type", 'object_id', "valid_period")




# ############ 2. 账户相关 #############

class Account(models.Model):
    """用户账户"""
    username = models.CharField("用户名", max_length=64, unique=True)
    email = models.EmailField(verbose_name='邮箱', max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(verbose_name='密码', max_length=128)

    def __str__(self):
        return self.username


class UserAuthToken(models.Model):
    """
    用户Token表
    """
    user = models.OneToOneField(to="Account")
    token = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user



    def save(self, *args, **kwargs):
        self.token = self.generate_key()
        self.created = datetime.datetime.utcnow()
        return super(UserAuthToken, self).save(*args, **kwargs)

    def generate_key(self):
        """根据用户名和时间生成唯一标识"""
        username = self.user.username
        now = str(datetime.datetime.now()).encode('utf-8')
        md5 = hashlib.md5(username.encode('utf-8'))
        md5.update(now)
        return md5.hexdigest()


# ############ 5. 深科技 #############
class ArticleSource(models.Model):
    """文章来源"""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章资讯"""
    title = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="文章标题")
    source = models.ForeignKey("ArticleSource", verbose_name="来源")
    article_type_choices = ((1, '资讯'), (2, '视频'))
    article_type = models.SmallIntegerField(choices=article_type_choices, default=1)
    brief = models.TextField(max_length=512, verbose_name="摘要")
    head_img = models.CharField(max_length=255, verbose_name='文章图片')
    content = models.TextField(verbose_name="文章正文")

    pub_date = models.DateTimeField(verbose_name="上架日期")
    offline_date = models.DateTimeField(verbose_name="下架日期")
    status_choices = ((1, '在线'), (2, '下线'))
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="状态")
    order = models.SmallIntegerField(default=0, verbose_name="权重", help_text="文章想置顶，可以把数字调大，不要超过1000")

    vid = models.CharField(max_length=128, verbose_name="视频VID", help_text="文章类型是视频, 则需要添加视频VID", blank=True, null=True)
    comment_num = models.SmallIntegerField(default=0, verbose_name="评论数")
    agree_num = models.SmallIntegerField(default=0, verbose_name="点赞数")
    view_num = models.SmallIntegerField(default=0, verbose_name="观看数")
    collect_num = models.SmallIntegerField(default=0, verbose_name="收藏数")

    # tags = models.ManyToManyField("Tags", blank=True, verbose_name="标签")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    position_choices = ((1, '信息流'), (2, 'banner大图'), (3, 'banner小图'))
    position = models.SmallIntegerField(choices=position_choices, default=1, verbose_name="位置")
    comment = GenericRelation("Comment", help_text='用于GenericForeignKey反向查询,不会生成表字段，切勿删除')

    def __str__(self):
        return self.title


class Collection(models.Model):
    """收藏"""
    account = models.ForeignKey("Account", verbose_name='用户')

    content_type = models.ForeignKey(ContentType, verbose_name='文章或视频表')
    object_id = models.PositiveIntegerField(verbose_name='文章或者视频ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'account')


class Comment(models.Model):
    """通用的评论表"""
    account = models.ForeignKey("Account", verbose_name="用户")

    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="文章或视频表")
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name='文章或者视频ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    p_node = models.ForeignKey("self", blank=True, null=True, verbose_name="父级评论")
    content = models.TextField(max_length=1024)

    disagree_number = models.IntegerField(default=0, verbose_name="踩")
    agree_number = models.IntegerField(default=0, verbose_name="赞同数")
    date = models.DateTimeField(auto_now_add=True)
