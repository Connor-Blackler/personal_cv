# Generated by Django 4.2.1 on 2023-06-07 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_education_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='education',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
