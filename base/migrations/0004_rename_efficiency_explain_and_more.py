# Generated by Django 4.1.1 on 2022-10-18 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_efficiency'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Efficiency',
            new_name='Explain',
        ),
        migrations.RenameField(
            model_name='explain',
            old_name='efficient',
            new_name='explain',
        ),
    ]