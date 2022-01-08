# Generated by Django 4.0 on 2022-01-07 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_billproduct_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Submitted', 'Submitted')], default='Submitted', max_length=11),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Submitted', 'Submitted')], default='Pending', max_length=11),
        ),
    ]