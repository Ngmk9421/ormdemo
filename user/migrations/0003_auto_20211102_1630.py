# Generated by Django 2.2 on 2021-11-02 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='icon',
            field=models.ImageField(upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mail',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=11, null=True),
        ),
    ]