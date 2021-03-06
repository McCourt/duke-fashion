# Generated by Django 2.1.2 on 2018-11-08 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biddingprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('closed', models.BooleanField(default=False)),
                ('openuntil', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerid', models.IntegerField()),
                ('orginalprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sellprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('condition', models.CharField(max_length=20)),
                ('size', models.CharField(max_length=3)),
                ('color', models.CharField(max_length=256)),
                ('brand', models.CharField(max_length=256)),
                ('ctype', models.CharField(max_length=256)),
                ('imgpath', models.CharField(max_length=256)),
                ('closed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collegeid', models.IntegerField()),
                ('username', models.CharField(max_length=256)),
                ('phone', models.DecimalField(decimal_places=0, max_digits=10)),
                ('email', models.CharField(max_length=256)),
                ('is_available', models.BooleanField()),
                ('is_end_product', models.BooleanField()),
                ('numtrade', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='bidding',
            name='clothes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fashion.Clothes'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fashion.Person'),
        ),
    ]
