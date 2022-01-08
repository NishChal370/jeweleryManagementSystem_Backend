# Generated by Django 4.0 on 2022-01-07 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_billproduct_billid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='orderId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.order'),
        ),
        migrations.AlterField(
            model_name='billproduct',
            name='billId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bill', to='main.bill'),
        ),
        migrations.AlterField(
            model_name='billproduct',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='main.product'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderProducts', to='main.product'),
        ),
    ]
