# Generated by Django 4.0.4 on 2022-10-13 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appblogs', '0007_blog_tema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='tema',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Tema do BLOG'),
        ),
    ]
