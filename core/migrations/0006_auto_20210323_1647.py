# Generated by Django 3.1.6 on 2021-03-23 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210323_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='profile_picture',
            field=models.URLField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='investor',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]