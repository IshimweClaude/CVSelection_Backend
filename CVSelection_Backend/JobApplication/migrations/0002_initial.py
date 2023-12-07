# Generated by Django 5.0 on 2023-12-04 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('JobApplication', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.applicant'),
        ),
        migrations.AddField(
            model_name='formal_education',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.applicant'),
        ),
        migrations.AddField(
            model_name='formal_education',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.country'),
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='JobApplication.job'),
        ),
        migrations.AddField(
            model_name='language_skills',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.applicant'),
        ),
        migrations.AddField(
            model_name='work_experience',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.applicant'),
        ),
        migrations.AddField(
            model_name='work_experience',
            name='working_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.country'),
        ),
    ]
