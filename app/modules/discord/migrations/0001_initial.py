# Generated by Django 2.0.3 on 2018-05-05 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordGroup',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='DiscordUser',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(to='discord.DiscordGroup')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
