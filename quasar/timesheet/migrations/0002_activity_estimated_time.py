# Generated by Django 3.2 on 2021-05-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='estimated_time',
            field=models.IntegerField(default=5, help_text='Estimated time in minutes.'),
        ),
    ]