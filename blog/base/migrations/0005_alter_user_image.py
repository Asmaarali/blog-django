# Generated by Django 4.2.5 on 2023-10-16 22:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0004_alter_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(
                default="static/images/avatar.svg", null=True, upload_to=""
            ),
        ),
    ]