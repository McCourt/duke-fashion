# Generated by Django 2.1.2 on 2018-11-08 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='sellerid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fashion.Person'),
        ),
    ]
