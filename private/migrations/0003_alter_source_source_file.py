# Generated by Django 3.2.9 on 2021-12-07 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private', '0002_alter_source_source_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='source_file',
            field=models.FileField(upload_to='priv/'),
        ),
    ]
