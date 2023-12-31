# Generated by Django 5.0 on 2023-12-07 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobApplication', '0008_alter_application_unique_together_alter_job_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('reviewed', 'Reviewed'), ('interviewed', 'Interviewed'), ('shortlisted', 'Shortlisted'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('hired', 'Hired')], default='submitted', max_length=100),
        ),
    ]
