# Generated by Django 2.0.3 on 2018-05-25 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discourseuser',
            name='linked',
            field=models.NullBooleanField(default=None),
        ),
    ]