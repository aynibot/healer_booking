# Generated by Django 2.0 on 2018-08-26 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20180826_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
