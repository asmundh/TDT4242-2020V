# Generated by Django 2.1.7 on 2020-03-07 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200116_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivery_rating',
            field=models.IntegerField(default=0),
        ),
    ]
