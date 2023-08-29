# Generated by Django 4.1.1 on 2022-10-18 17:22

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_efficiency_explain_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_from', models.TextField(verbose_name=base.models.Language)),
                ('language_to', models.TextField(verbose_name=base.models.Language)),
                ('translate', models.TextField(max_length=4000)),
            ],
        ),
        migrations.AlterField(
            model_name='explain',
            name='explain',
            field=models.TextField(max_length=4000),
        ),
    ]