# Generated by Django 4.0 on 2022-01-06 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customerId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.customer'),
        ),
    ]