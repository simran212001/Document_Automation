# Generated by Django 4.1.7 on 2023-05-08 07:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_dia', '0003_context_srs_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.CharField(max_length=50)),
                ('action', models.CharField(max_length=50)),
                ('fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=[], size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
