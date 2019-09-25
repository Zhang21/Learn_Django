import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

"""
代码非常直白，每个模型被表示为django.db.models.Model类的子类。每个模型有一些类变量，它们都表示模型里的一个数据库字段。
每个字段都是Field类的实例，比如，字符字段被表示为CharField，日期时间字段被表示为DateTimeField。这将告诉Django每个字段要处理的数据类型。
定义某些Field类实例需要参数。例如CharField需要一个max_length参数。这个参数的用处不止于用来定义数据库结构，也用于验证数据。
使用ForeignKey定义了一个关系，这将告诉Django，每个Choice对象都关联到一个Question对象。Django支持所有常用的数据库关系：一对一、一对多、多对多。

这段代码为应用创建数据库schema(CREATE TABLE)
创建可与Question和Choice对象进行交互的Python数据库API
"""


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_data = models.DateTimeField('date published')

    # 给模型增加__str__()方法很重要
    def __str__(self):
        return self.question_text

    # 添加一个自定义的方法
    def was_published_recently(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
