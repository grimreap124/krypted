# Generated by Django 2.0.2 on 2018-03-27 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('slack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_id', models.CharField(max_length=64)),
                ('groups', models.ManyToManyField(blank=True, null=True, to='auth.Group')),
            ],
        ),
    ]
