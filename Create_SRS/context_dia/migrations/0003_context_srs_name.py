# Generated by Django 4.1.7 on 2023-04-12 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_dia', '0002_alter_context_entities'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='srs_name',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]