# Generated by Django 2.0 on 2018-08-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='customer_name',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]
