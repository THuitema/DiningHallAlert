# Generated by Django 4.2.13 on 2024-05-23 03:11

import accounts.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_user_email_ci_uniqueness'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='profile',
            name='user_email_ci_uniqueness',
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=accounts.fields.LowercaseEmailField(max_length=255, unique=True),
        ),
    ]
