# Generated by Django 2.0.3 on 2018-05-05 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evecharacter',
            name='token',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='eveonline.Token'),
        ),
    ]
