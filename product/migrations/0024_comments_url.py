# Generated by Django 4.1.2 on 2022-12-03 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_remove_item_in_cart_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='url',
            field=models.URLField(default='profile'),
            preserve_default=False,
        ),
    ]
