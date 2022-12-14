# Generated by Django 4.1.2 on 2022-11-30 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0011_donation_is_taken'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('message', models.CharField(max_length=64)),
                ('data_send', models.DateTimeField()),
            ],
        ),
    ]
