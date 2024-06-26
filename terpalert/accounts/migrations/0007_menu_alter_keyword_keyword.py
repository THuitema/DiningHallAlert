# Generated by Django 4.2.13 on 2024-05-24 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_keyword_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.menu'),
        ),
    ]
