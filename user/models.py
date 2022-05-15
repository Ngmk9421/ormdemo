from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=25, unique=True, null=False, blank=False)
    password = models.CharField(max_length=120, null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class UserProfile(models.Model):
    gender = models.BooleanField(default=0, null=True)
    phone = models.CharField(max_length=11, null=True)
    mail = models.CharField(max_length=50, null=True)
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'userprofile'


class Message(models.Model):
    send_id = models.IntegerField()
    receive_id = models.IntegerField()
    msg = models.TextField(null=False)
    is_delete = models.BooleanField(default=False)
    send_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
