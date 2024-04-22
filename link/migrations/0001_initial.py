# Generated by Django 4.1 on 2024-04-14 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrlModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.CharField(blank=True, max_length=300, null=True, unique=True)),
                ('long_url', models.CharField(blank=True, max_length=300, null=True)),
                ('clicks', models.BigIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('premium', models.BooleanField(blank=True, null=True)),
                ('last_access', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]