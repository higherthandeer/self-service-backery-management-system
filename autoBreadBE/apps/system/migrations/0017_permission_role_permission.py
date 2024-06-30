# Generated by Django 4.2.8 on 2024-03-15 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0016_alter_user_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="Permission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="权限名称",
                        max_length=100,
                        unique=True,
                        verbose_name="权限名称",
                    ),
                ),
                (
                    "level",
                    models.IntegerField(
                        blank=True,
                        help_text="权限名称",
                        max_length=10,
                        null=True,
                        verbose_name="权限名称",
                    ),
                ),
                (
                    "select",
                    models.BooleanField(
                        default=False, help_text="权限名称", verbose_name="权限名称"
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="权限名称",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="system.permission",
                        verbose_name="权限名称",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="role",
            name="permission",
            field=models.ManyToManyField(
                help_text="权限", to="system.permission", verbose_name="权限"
            ),
        ),
    ]
