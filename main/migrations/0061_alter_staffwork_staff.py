# Generated by Django 4.0 on 2022-02-15 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0060_staffwork_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffwork',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffwork', to='main.staff'),
        ),
    ]