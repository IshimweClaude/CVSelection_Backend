from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Country
from .serializers import *
from django.utils import timezone
from django.db import IntegrityError
# Record AFDB countries
from rest_framework import status
import json
from django_filters.rest_framework import DjangoFilterBackend


class CountryCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can add new countries."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Country added successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all countries
class CountryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country_name','isMemberOfAFDB','id']

    def get(self, request):
        countries = Country.objects.all()
        if countries:
            serializer = CountrySerializer(countries, many=True)
            return Response({"message": "Countries fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No countries found."}, status=status.HTTP_404_NOT_FOUND)
    

# Record AFDB jobs
class JobCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can add new jobs."}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job added successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# List all jobs

class JobListView(APIView):
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    
    filterset_fields = ['title','location','status','job_type','id','salary','postedDate','deadline']
    authentication_classes = []
    def get(self, request):
        jobs = Job.objects.filter(status='open')
        if jobs:
            serializer = JobSerializer(jobs, many=True)
            return Response({"message": "Jobs fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No jobs found."}, status=status.HTTP_404_NOT_FOUND)


# Record AFDB formal education as part of applicant's profile

# class Formal_educationCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         if request.user.user_role != 'applicant':
#             return Response({"detail": "Sorry, only applicants can add formal education."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = Formal_educationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Formal education added successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# list my formal education

# class Formal_educationListView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         formal_education = Formal_education.objects.filter(applicant=request.user)
#         if formal_education:
#             serializer = Formal_educationSerializer(formal_education, many=True)
#             return Response({"message": "Formal education fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "No formal education found."}, status=status.HTTP_404_NOT_FOUND)
        
# Record AFDB work experience as part of applicant's profile

# class Work_experienceCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         if request.user.user_role != 'applicant':
#             return Response({"detail": "Sorry, only applicants can add work experience."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = Work_experienceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Work experience added successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# list my work experience

# class Work_experienceListView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         work_experience = Work_experience.objects.filter(applicant=request.user)
#         if work_experience:
#             serializer = Work_experienceSerializer(work_experience, many=True)
#             return Response({"message": "Work experience fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "No work experience found."}, status=status.HTTP_404_NOT_FOUND)
        

# Record AFDB language skills as part of applicant's profile

# class Language_skillsCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         if request.user.user_role != 'applicant':
#             return Response({"detail": "Sorry, only applicants can add language skills."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = Language_skillsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Language skills added successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# list my language skills

# class Language_skillsListView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         language_skills = Language_skills.objects.filter(applicant=request.user)
#         if language_skills:
#             serializer = Language_skillsSerializer(language_skills, many=True)
#             return Response({"message": "Language skills fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "No language skills found."}, status=status.HTTP_404_NOT_FOUND)
        

class JobApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_id):
        # Check if the job exists and has not reached the deadline
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        if job.deadline < timezone.now().date():
            return Response({"detail": "Job application deadline has passed."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user is an applicant
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicants can apply for jobs."}, status=status.HTTP_403_FORBIDDEN)

        # Create the application
        application_data = request.data
        application_data['applicant'] = request.user
        application_data['job'] = job.id
        application_serializer = ApplicationSerializer(data=application_data)
        if application_serializer.is_valid():
            try:
                application_serializer.save()
            except IntegrityError:
                return Response({"detail": "You have already applied for this job."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(application_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create the formal education
        formal_educations_data = request.data.get('formal_educations')
        if formal_educations_data is not None:
            try:
                formal_educations_data = json.loads(formal_educations_data)
            except json.JSONDecodeError:
                return Response({"detail": "Invalid data. 'formal_educations' should be a JSON string."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(formal_educations_data, list):
            return Response({"detail": "Invalid data. 'formal_educations' should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        for formal_education_data in formal_educations_data:
            formal_education_data['applicant'] = request.user.id
            try:
                country = Country.objects.get(country_name=formal_education_data['country'])
            except Country.DoesNotExist:
                return Response({"detail": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
            formal_education_data['country'] = country.id
            formal_education_serializer = Formal_educationSerializer(data=formal_education_data)
            if formal_education_serializer.is_valid():
                formal_education_serializer.save()
            else:
                return Response(formal_education_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

       # Create the work experience
        work_experiences_data = request.data.get('work_experiences')
        if work_experiences_data is not None:
            try:
                work_experiences_data = json.loads(work_experiences_data)
            except json.JSONDecodeError:
                return Response({"detail": "Invalid data. 'work_experiences' should be a JSON string."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(work_experiences_data, list):
            return Response({"detail": "Invalid data. 'work_experiences' should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        for work_experience_data in work_experiences_data:
            work_experience_data['applicant'] = request.user.id
            try:
                country = Country.objects.get(country_name=work_experience_data['working_country'])
            except Country.DoesNotExist:
                return Response({"detail": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
            work_experience_data['working_country'] = country.id
            work_experience_serializer = Work_experienceSerializer(data=work_experience_data)
            if work_experience_serializer.is_valid():
                work_experience_serializer.save()
            else:
                return Response(work_experience_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Create the language skills
        language_skills_data = request.data.get('language_skills')
        if language_skills_data is not None:
            try:
                language_skills_data = json.loads(language_skills_data)
            except json.JSONDecodeError:
                return Response({"detail": "Invalid data. 'language_skills' should be a JSON string."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(language_skills_data, list):
            return Response({"detail": "Invalid data. 'language_skills' should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        for language_skill_data in language_skills_data:
            language_skill_data['applicant'] = request.user.id
            language_skills_serializer = Language_skillsSerializer(data=language_skill_data)
            if language_skills_serializer.is_valid():
                language_skills_serializer.save()
            else:
                return Response(language_skills_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": "Job application submitted successfully!"}, status=status.HTTP_201_CREATED)
    


