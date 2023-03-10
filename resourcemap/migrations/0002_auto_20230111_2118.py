# Generated by Django 3.2.5 on 2023-01-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourcemap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='assettype',
            field=models.CharField(choices=[('LAPTOP', 'LAPTOP'), ('TRAVEL_BAG', 'TRAVEL_BAG'), ('PACKAGE', 'PACKAGE')], max_length=200),
        ),
        migrations.AlterField(
            model_name='requests',
            name='deliverby',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requests',
            name='packagesensitivity',
            field=models.CharField(choices=[('HIGHLY_SENSITIVE', 'HIGHLY_SENSITIVE'), ('SENSITIVE', 'SENSITIVE'), ('NORMAL', 'NORMAL')], max_length=200),
        ),
    ]
