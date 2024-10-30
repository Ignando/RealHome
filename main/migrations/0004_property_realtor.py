# Generated by Django 5.1 on 2024-10-29 22:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_favorite'),
        ('realtors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='realtor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='properties', to='realtors.realtor'),
        ),
    ]
