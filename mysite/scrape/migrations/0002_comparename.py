# Generated by Django 4.2.5 on 2023-11-01 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompareName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]