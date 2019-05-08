# Generated by Django 2.1.2 on 2018-12-06 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0004_auto_20181108_0458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothes',
            name='imgpath',
        ),
        migrations.AddField(
            model_name='clothes',
            name='details',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='clothes',
            name='image',
            field=models.ImageField(default='images/dukeshirt.png', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='size',
            field=models.CharField(max_length=20),
        ),
    ]