# Generated by Django 5.2.3 on 2025-06-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(default=10),
        ),
    ]
