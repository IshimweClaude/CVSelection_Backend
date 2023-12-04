from rest_framework import viewsets
from .import models
from .import serializers

class JobViewset(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    
class Formal_educationViewset(viewsets.ModelViewSet):
    queryset = models.Formal_education.objects.all()
    serializer_class = serializers.Formal_educationSerializer

class Work_experienceViewset(viewsets.ModelViewSet):
    queryset = models.Work_experience.objects.all()
    serializer_class = serializers.Work_experienceSerializer

class Language_skillsViewset(viewsets.ModelViewSet):
    queryset = models.Language_skills.objects.all()
    serializer_class = serializers.Language_skillsSerializer    

class ApplicationViewset(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
