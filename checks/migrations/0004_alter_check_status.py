# Generated by Django 4.0.4 on 2022-05-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0003_check_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='status',
            field=models.IntegerField(choices=[(1, 'new'), (2, 'rendered')]),
        ),
    ]
