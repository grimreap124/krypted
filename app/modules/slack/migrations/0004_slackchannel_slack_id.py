# Generated by Django 2.0.3 on 2018-06-07 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0003_remove_slackchannel_slack_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='slackchannel',
            name='slack_id',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
