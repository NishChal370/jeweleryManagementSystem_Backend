# Generated by Django 4.0 on 2022-01-07 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_bill_advanceamount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='customerId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='main.customer'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='orderId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='rate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
