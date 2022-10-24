# Generated by Django 4.1.2 on 2022-10-22 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_remove_user_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('FUNDATION', 'Fundacja'), ('NON-GOVERMENTAL ORGANISATION', 'Organizacja pozarządowa'), ('LOCAL COLLECTION', 'Zbiórka lokalna')], default='FUNDATION', max_length=64)),
                ('categories', models.ManyToManyField(to='donations.category')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField()),
                ('address', models.CharField(max_length=256)),
                ('phone_number', models.PositiveBigIntegerField()),
                ('city', models.CharField(max_length=64)),
                ('zip_code', models.PositiveIntegerField()),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.CharField(max_length=1024)),
                ('categories', models.ManyToManyField(to='donations.category')),
                ('institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.institution')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
