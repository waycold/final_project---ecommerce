# Generated by Django 4.1.2 on 2022-11-30 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_profile_description_alter_profile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='in_cart',
            field=models.BooleanField(default=False),
        ),
    ]