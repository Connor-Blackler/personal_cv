# Generated by Django 4.2.1 on 2023-06-07 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_education_description_alter_education_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='title',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='title',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='language',
            name='color',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='language',
            name='title',
            field=models.CharField(max_length=500, primary_key=True, serialize=False),
        ),
    ]
