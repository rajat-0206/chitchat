# Generated by Django 3.0.8 on 2020-07-20 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200718_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='changepassword',
            name='u_name',
            field=models.CharField(default='Null', max_length=20),
        ),
    ]