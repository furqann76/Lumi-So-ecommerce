# Generated by Django 5.2.3 on 2025-06-29 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_product_stock"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="sentiment",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
