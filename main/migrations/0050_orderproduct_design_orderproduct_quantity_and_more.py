# Generated by Django 4.0 on 2022-02-09 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_remove_order_design_order_billtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='design',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='quantity',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('inprogress', 'INPROGRESS'), ('submitted', 'SUBMITTED')], default='pending', max_length=11),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
