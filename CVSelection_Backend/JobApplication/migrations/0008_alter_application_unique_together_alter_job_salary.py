# Generated by Django 5.0 on 2023-12-07 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobApplication', '0007_alter_application_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
