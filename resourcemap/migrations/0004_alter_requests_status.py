# Generated by Django 3.2.5 on 2023-01-11 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourcemap', '0003_alter_rides_travelmedium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
