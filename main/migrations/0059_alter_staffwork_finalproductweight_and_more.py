# Generated by Django 4.0 on 2022-02-15 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_rename_registration_date_staff_registrationdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffwork',
            name='finalProductWeight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffwork',
            name='lossWeight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffwork',
            name='submittedWeight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]