# Generated by Django 3.0.2 on 2020-03-09 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_pet_services_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet_services',
            name='mpesa_receipt_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
