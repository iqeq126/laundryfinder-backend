# Generated by Django 4.2.1 on 2023-06-01 02:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crud", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="images",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]