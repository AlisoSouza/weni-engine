# Generated by Django 2.2.19 on 2021-03-22 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0005_auto_20210319_1816"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsletter",
            name="title",
            field=models.CharField(max_length=50, verbose_name="title"),
        ),
    ]