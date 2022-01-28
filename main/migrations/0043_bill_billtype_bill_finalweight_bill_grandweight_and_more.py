# Generated by Django 4.0 on 2022-01-28 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_rename_qualtity_billproduct_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='billType',
            field=models.CharField(choices=[('gold', 'GOLD'), ('silver', 'SILVER')], default='gold', max_length=11),
        ),
        migrations.AddField(
            model_name='bill',
            name='finalWeight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='grandWeight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='status',
            field=models.CharField(choices=[('draft', 'DRAFT'), ('submitted', 'SUBMITTED')], default='submitted', max_length=11),
        ),
    ]
