# Generated by Django 4.1.2 on 2022-10-26 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0005_alter_institution_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='categories',
            field=models.ManyToManyField(related_name='donation_vategories', to='donations.category'),
        ),
    ]
