# Generated by Django 4.1.2 on 2022-11-21 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_item_category_alter_item_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
