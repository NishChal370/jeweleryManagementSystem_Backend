# Generated by Django 4.0 on 2022-02-09 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='netWeight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]