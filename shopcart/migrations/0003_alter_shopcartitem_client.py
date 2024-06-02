# Generated by Django 3.2.4 on 2021-07-07 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopcart', '0002_shopcartitem_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcartitem',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shopcart_item', to=settings.AUTH_USER_MODEL),
        ),
    ]