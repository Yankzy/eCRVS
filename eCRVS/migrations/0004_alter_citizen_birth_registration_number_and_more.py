# Generated by Django 4.1.5 on 2023-02-10 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCRVS', '0003_delete_utility_delete_weebhookreceived_citizen_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='birth_registration_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='dob',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='first_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='last_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='nin',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='uin',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
