# Generated by Django 3.0.8 on 2020-07-10 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarker', '0002_auto_20200709_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videodata',
            name='timeStamps',
            field=models.TextField(blank=True, null=True),
        ),
    ]
