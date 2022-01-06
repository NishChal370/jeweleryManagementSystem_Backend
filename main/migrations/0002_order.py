# Generated by Django 4.0 on 2022-01-06 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('rate', models.IntegerField(null=True)),
                ('advanceAmount', models.IntegerField(null=True)),
                ('submittionDate', models.DateField()),
                ('submittedDate', models.DateField(null=True)),
                ('design', models.ImageField(blank=True, null=True, upload_to='')),
                ('status', models.TextField(null=True)),
                ('remark', models.TextField(null=True)),
                ('customerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
            ],
        ),
    ]