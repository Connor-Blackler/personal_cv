# Generated by Django 4.2.1 on 2023-06-06 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_education_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='state',
            field=models.CharField(choices=[('Completed', 'COMPLETED'), ('In-progress', 'IN_PROGRESS'), ('Not-started', 'NOT_STARTED')], max_length=100),
        ),
    ]
