# Generated by Django 2.2.24 on 2021-07-27 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0028_billingplan_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="billingplan",
            name="stripe_customer",
            field=models.CharField(
                blank=True,
                help_text="Our Stripe customer id for your organization",
                max_length=32,
                null=True,
                verbose_name="Stripe Customer",
            ),
        ),
    ]