# Generated by Django 4.0.4 on 2022-10-11 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appblogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='UID',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Código UID do Blog'),
        ),
        migrations.AddField(
            model_name='post',
            name='UID',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Código UID do POST'),
        ),
    ]
