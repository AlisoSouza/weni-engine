# Generated by Django 3.2.6 on 2021-08-16 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0028_auto_20210816_1343"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="cost_per_whatsapp",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=11,
                verbose_name="cost per whatsapp",
            ),
        ),
    ]
