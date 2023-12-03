from rest_framework import serializers
from .models import Job,Formal_education,Work_experience,Language_skills,Application

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_id', 'title', 'description', 'requirements', 'postedDate', 'deadline', 'location', 'status']

class Formal_educationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formal_education
        fields = ['formal_education_id', 'institution', 'degree', 'start_date', 'end_date', 'country', 'applicant', 'subject', 'grade']

class Work_experienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_experience
        fields = ['work_experience_id', 'company_name', 'start_date', 'is_present_employee', 'working_country', 'applicant', 'industry', 'job_title']

class Language_skillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language_skills
        fields = ['language_skills_id', 'language', 'reading', 'writing', 'speaking', 'applicant']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['application_id', 'applicant', 'job', 'date_applied', 'cv']


