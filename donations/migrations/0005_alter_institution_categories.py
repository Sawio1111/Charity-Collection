# Generated by Django 4.1.2 on 2022-10-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_alter_donation_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='categories',
            field=models.ManyToManyField(related_name='categories', to='donations.category'),
        ),
    ]
