# Generated by Django 4.2.13 on 2024-05-24 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_menu_alter_keyword_keyword'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyword',
            old_name='keyword',
            new_name='menu_item',
        ),
    ]
