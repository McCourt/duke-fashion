# Generated by Django 2.1.2 on 2018-11-08 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fashion', '0003_auto_20181108_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='collegeid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='person',
            name='numtrade',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(default='', max_length=256),
        ),
    ]
