# Generated by Django 4.2.7 on 2023-12-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobApplication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language_skills',
            name='reading',
            field=models.CharField(choices=[('basic', 'Basic'), ('intermediate', 'Intermediate'), ('h', 'Advanced'), ('fluent', 'Fluent'), ('native', 'Native')], max_length=100),
        ),
        migrations.AlterField(
            model_name='language_skills',
            name='speaking',
            field=models.CharField(choices=[('basic', 'Basic'), ('intermediate', 'Intermediate'), ('h', 'Advanced'), ('fluent', 'Fluent'), ('native', 'Native')], max_length=100),
        ),
        migrations.AlterField(
            model_name='language_skills',
            name='writing',
            field=models.CharField(choices=[('basic', 'Basic'), ('intermediate', 'Intermediate'), ('h', 'Advanced'), ('fluent', 'Fluent'), ('native', 'Native')], max_length=100),
        ),
    ]
