# Generated by Django 4.2.3 on 2023-07-09 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
        migrations.AddField(
            model_name='author',
            name='pseudonym',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
    ]
