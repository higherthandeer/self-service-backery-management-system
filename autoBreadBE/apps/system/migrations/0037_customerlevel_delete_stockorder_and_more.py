# Generated by Django 4.2.8 on 2024-05-13 21:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0036_customerlevel_delete_stockorder_inventory_goods_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permission",
            name="is_button",
            field=models.BooleanField(
                default=0, help_text="是否为按钮", verbose_name="是否为按钮"
            ),
        ),
    ]
