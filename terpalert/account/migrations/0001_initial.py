# Generated by Django 5.0.4 on 2024-05-06 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.CharField(blank=True, max_length=320, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.users')),
            ],
        ),
    ]
