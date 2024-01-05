from rest_framework import serializers
from .models import Job,Formal_education,Work_experience,Language_skills,Application
from authentication.models import Country,Applicant



class CountrySerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='country',queryset=Country.objects.all())
    class Meta:
        model = Country
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class Formal_educationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formal_education
        fields = "__all__"

class Work_experienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_experience
        fields = "__all__"


class Language_skillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language_skills
        fields = "__all__"
class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"



