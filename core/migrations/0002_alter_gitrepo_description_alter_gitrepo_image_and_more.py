# Generated by Django 4.2.1 on 2023-05-31 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitrepo',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='image',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='repos', to='core.language'),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='url',
            field=models.URLField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='language',
            name='color',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='language',
            name='title',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
