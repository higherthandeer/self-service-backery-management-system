# Generated by Django 4.2.8 on 2024-05-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0039_customerlevel_delete_stockorder_and_more"),
    ]

    operations = [

        migrations.AlterField(
            model_name="receiptitem",
            name="breadname",
            field=models.CharField(
                help_text="面包名称", max_length=64, verbose_name="面包名称"
            ),
        ),
        migrations.AlterField(
            model_name="receiptitem",
            name="price",
            field=models.DecimalField(
                decimal_places=2, help_text="单价", max_digits=10, verbose_name="单价"
            ),
        ),
    ]
