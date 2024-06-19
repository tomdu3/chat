# Generated by Django 5.0.6 on 2024-06-19 19:21

import server.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="",
                verbose_name=server.models.category_icon_upload_path,
            ),
        ),
        migrations.AlterField(
            model_name="server",
            name="description",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]