# Generated by Django 3.0.1 on 2020-04-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='answers',
            field=models.IntegerField(default=0, verbose_name='comment answers'),
        ),
    ]