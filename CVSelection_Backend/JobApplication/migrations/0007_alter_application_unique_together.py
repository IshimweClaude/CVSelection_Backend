# Generated by Django 5.0 on 2023-12-07 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JobApplication', '0006_alter_application_status'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('applicant', 'job')},
        ),
    ]
