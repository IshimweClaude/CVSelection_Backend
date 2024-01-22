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
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField() # job description
    requirements = models.TextField()
    postedDate = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='open')
    job_type = models.CharField(max_length=100, choices=JOB_TYPE_CHOICES, default='full_time')
    english_job_description = models.FileField(upload_to='english_job_description_file/',default=None)
    french_job_description = models.FileField(upload_to='french_job_description_file/',default=None)

    class Meta:
        ordering = ['-postedDate']
        db_table = 'job'
    
class Formal_education(models.Model):
    DEGREE_CHOICES = [
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('PhD', 'PhD'),
        ('Associate', 'Associate'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
        ('Other', 'Other'),
    ]
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100, choices=DEGREE_CHOICES) # Bachelor, Master, PhD, etc.
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True) 
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100) # To be choosen. eg: Computer Science, Business Administration, etc.
    grade = models.CharField(max_length=100, blank=True, null=True) # GPA

    class Meta:
        ordering = ['-start_date']
        db_table = 'formal_education'

class Work_experience(models.Model):
    JOB_TITLE_CHOICES = [
        ('Software Engineer', 'Software Engineer'),
        ('Business Analyst', 'Business Analyst'),
        # Add more job titles as needed
    ]
    INDUSTRY_CHOICES = [
        ('Agriculture', 'Agriculture'),
        ('Banking', 'Banking'),
        ('Health', 'Health'),
        # Add more industries as needed
    ]
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    is_present_employee = models.BooleanField(default=False) # if . true, no end_date (To be done on frontEnd)
    end_date = models.DateField(default=None, blank=True, null=True)
    working_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True, null=True) # Agriculture, Banking, Health, etc.
    job_title = models.CharField(max_length=100, choices=JOB_TITLE_CHOICES, blank=True, null=True) # To be chosen. eg: Software Engineer, Business Analyst, etc.

    class Meta:
        ordering = ['-start_date']
        db_table = 'work_experience'

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
        ('advanced', 'Advanced'),
        ('fluent', 'Fluent'),
        ('native', 'Native'),
    ]
    
    # languagues list. eg: English, French, Arabic, etc.
    language = models.CharField(max_length=100, choices=LANGUAGE_NAME_CHOICES)
    # Proficiency levels. eg: Basic, Intermediate, Advanced, Fluent, Native
    reading = models.CharField(max_length=100, choices=LEVEL_CHOICES) 
    writing = models.CharField(max_length=100,choices=LEVEL_CHOICES)
    speaking = models.CharField(max_length=100,choices=LEVEL_CHOICES)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)


    class Meta:
        db_table = 'language_skills'

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
    
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='submitted')
    date_applied = models.DateField(auto_now_add=True)
    cv = models.FileField(upload_to='application_files/')
    cover_letter = models.FileField(upload_to='application_files/', blank=True, null=True)

    def __str__(self):
        return f'{self.applicant} applied for {self.job}'

    class Meta:
        ordering = ['-date_applied']
        db_table = 'application'
        # unique_together = ['applicant', 'job']


        