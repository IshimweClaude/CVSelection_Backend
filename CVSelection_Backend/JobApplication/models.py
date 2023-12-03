from django.db import models
from django.conf import settings
from authentication.models import Applicant
from authentication.models import Country

# Create your models here.


class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),

    ]
    job_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField() # job description
    requirements = models.TextField(max_length=100)
    postedDate = models.DateField(auto_now=True)
    deadline = models.DateField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='open')

    job_file = models.FileField(upload_to='job_file/', blank=True, null=True)
    
class Formal_education(models.Model):
    formal_education_id = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100) # Bachelor, Master, PhD, etc.
    start_date = models.DateField()
    end_date = models.DateField() 
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=100, blank=True, null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100) # To be choosen. eg: Computer Science, Business Administration, etc.
    grade = models.CharField(max_length=100) # GPA
    
class Work_experience(models.Model):
    
    work_experience_id = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    is_present_employee = models.BooleanField(default=False) # if . true, no end_date (To be done on frontEnd)
    end_date = models.DateField(default=None, blank=True, null=True)
    working_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField(max_length=100,blank=True, null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    industry = models.CharField(max_length=100) # Agriculcilure, Banking, Health, etc.
    job_title = models.CharField(max_length=100) # To be choosen. eg: Software Engineer, Business Analyst, etc.

class Language_skills(models.Model):
    LANGUAGE_NAME_CHOICES = [
        ('English', 'English'),
        ('French', 'French'),
        ('Arabic', 'Arabic'),
        ('Spanish', 'Spanish'),
        ('Portuguese', 'Portuguese'),
        ('Russian', 'Russian'),
        ('German', 'German'),
        ('Chinese', 'Chinese'),
        ('Japanese', 'Japanese'),
        ('Hindi', 'Hindi'),
        ('Turkish', 'Turkish'),
        ('Italian', 'Italian'),
        ('Persian', 'Persian'),
        ('Korean', 'Korean'),
        ('Vietnamese', 'Vietnamese'),
        ('Malay', 'Malay'),
        ('Kannada', 'Kannada'),
        ('Ukrainian', 'Ukrainian'),
        ('Romanian', 'Romanian'),
        ('Dutch', 'Dutch'),
        ('Kinyarwanda', 'Kinyarwanda'),
        ('Swahili', 'Swahili'),
        ('Mandarin', 'Mandarin'),
        ('Amharic', 'Amharic'),
        ('Yorùbá', 'Yorùbá'),
        ('Oromo', 'Oromo'),
        ('lingala', 'lingala'),
        
    ]
    LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('h', 'Advanced'),
        ('fluent', 'Fluent'),
        ('native', 'Native'),
    ]
    language_skills_id = models.CharField(max_length=100) 
    # languagues list. eg: English, French, Arabic, etc.
    language = models.CharField(max_length=100, choices=LANGUAGE_NAME_CHOICES)
    # Proficiency levels. eg: Basic, Intermediate, Advanced, Fluent, Native
    reading = models.CharField(max_length=100, choices=LEVEL_CHOICES) 
    writing = models.CharField(max_length=100,choices=LEVEL_CHOICES)
    speaking = models.CharField(max_length=100,choices=LEVEL_CHOICES)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

class Application(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('interviewed', 'Interviewed'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    application_id = models.CharField(max_length=100)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,default=1)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='submitted')
    date_applied = models.DateField()
    cv = models.FileField(upload_to='application_files/')
    cover_letter = models.FileField(upload_to='application_files/', blank=True, null=True)

    is_shortlisted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_hired = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_interviewed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Ensure only one of the is_* fields is True
        is_fields = [
            'is_shortlisted',
            'is_rejected',
            'is_hired',
            'is_submitted',
            'is_reviewed',
            'is_interviewed',
            'is_accepted',
            'is_rejected_by_recruiter',
        ]

        for field in is_fields:
            if getattr(self, field):
                for other_field in is_fields:
                    if other_field != field:
                        setattr(self, other_field, False)

        super().save(*args, **kwargs)
