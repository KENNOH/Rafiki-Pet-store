# Generated by Django 2.2 on 2020-01-14 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet_services',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
