# Generated by Django 3.1.5 on 2021-02-01 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='closing_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='opening_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
