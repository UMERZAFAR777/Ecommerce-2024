# Generated by Django 5.0.7 on 2024-08-10 04:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.color'),
        ),
    ]
