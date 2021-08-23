# Generated by Django 3.2.6 on 2021-08-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0027_invoice_capture_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="extra_integration",
            field=models.IntegerField(
                default=0, verbose_name="Whatsapp Extra Integration"
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="extra_integration",
            field=models.IntegerField(
                default=0, verbose_name="Whatsapp Extra Integration"
            ),
        ),
    ]
