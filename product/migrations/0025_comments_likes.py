# Generated by Django 4.1.2 on 2022-12-03 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_comments_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
