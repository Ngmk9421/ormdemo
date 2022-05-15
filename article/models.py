from django.db import models


# Create your models here.
from user.models import User


class Base(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Type(Base):
    tname = models.CharField(max_length=50, unique=True, null=False, blank=False)

    class Meta:
        db_table = 'type'


class Article(Base):
    title = models.CharField(max_length=50, null=False, blank=False)
    desc = models.CharField(max_length=200, null=False, blank=False)
    text = models.TextField(max_length=500, null=False, blank=False)
    save_num = models.IntegerField(default=0)
    like_num = models.IntegerField(default=0)
    visit_num = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    type = models.ForeignKey(to=Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'article'

