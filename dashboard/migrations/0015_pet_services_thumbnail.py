# Generated by Django 3.0.2 on 2020-03-09 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20200309_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet_services',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='dashboard'),
        ),
    ]
