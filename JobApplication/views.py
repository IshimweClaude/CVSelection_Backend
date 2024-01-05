from rest_framework import permissions, filters
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Country
from .serializers import *
from django.utils import timezone
from django.db import IntegrityError
# Record AFDB countries
from rest_framework import status
import json
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from authentication.models import Applicant
from django.core.exceptions import ObjectDoesNotExist

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country_name','isMemberOfAFDB','id']
    search_fields = ['country_name','isMemberOfAFDB','id']

    def get(self, request):
        countries = Country.objects.all()
        if countries:
            serializer = CountrySerializer(countries, many=True)
            return Response({"message": "Countries fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No countries found."}, status=status.HTTP_404_NOT_FOUND)
        
class CountryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country_name','isMemberOfAFDB','id']
    search_fields = ['country_name','isMemberOfAFDB','id']
    
    def get(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except Country.DoesNotExist:
            return Response({"detail": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CountrySerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except Country.DoesNotExist:
            return Response({"detail": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can update countries."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Country updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except Country.DoesNotExist:
            return Response({"detail": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can delete countries."}, status=status.HTTP_403_FORBIDDEN)
        country.delete()
        return Response({"message": "Country deleted successfully!"}, status=status.HTTP_200_OK)

# Record AFDB jobs
class JobCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['id','title','location','status','job_type','id','salary','postedDate','deadline']
    search_fields = ['id','title','location','status','job_type','id','salary','postedDate','deadline']

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
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['id','title','location','status','job_type','id','salary','postedDate','deadline']
    search_fields = ['id','title','location','status','job_type','id','salary','postedDate','deadline']
    authentication_classes = []
    
    def get(self, request):
        jobs = Job.objects.filter(status='open')
        
        if jobs:
            serializer = JobSerializer(jobs, many=True)
            return Response({"message": "Jobs fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No jobs found."}, status=status.HTTP_404_NOT_FOUND)


class JobDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['id','title','location','status','job_type','id','salary','postedDate','deadline']
    search_fields = ['id','title','location','status','job_type','id','salary','postedDate','deadline']
        
    def get(self, request, id):
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can update jobs."}, status=status.HTTP_403_FORBIDDEN)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can delete jobs."}, status=status.HTTP_403_FORBIDDEN)
        job.delete()
        return Response({"message": "Job deleted successfully!"}, status=status.HTTP_200_OK)
    

# ====================
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
        application_data = request.data.copy()
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
            
        
        applicant_id = request.user.id
        applicant_data = request.data.get('applicant')

        try:
            applicant_data = json.loads(applicant_data)
        except json.JSONDecodeError:
            return Response({"detail": "Invalid data. 'applicant' should be a JSON string."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the existing applicant object
        try:
            applicant = Applicant.objects.get(applicant_id=applicant_id)
        except Applicant.DoesNotExist:
            return Response({"detail": "Applicant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve the country object
        try:
            country = Country.objects.get(country_name=applicant_data.get('country'))
        except ObjectDoesNotExist:
            return Response({"detail": "Country not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the country in applicant_data
        applicant_data['country'] = country.id

        # Update the applicant object
        applicant_serializer = ApplicantSerializer(applicant, data=applicant_data, partial=True)
        if applicant_serializer.is_valid():
            applicant_serializer.save()
        else:
            return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

        return Response({"message": "Applicant Info updated successfully!"}, status=status.HTTP_200_OK)
# ========================================================================================================
class JobApplicationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can view job applications."}, status=status.HTTP_403_FORBIDDEN)

        applications = Application.objects.all()
        if applications:
            serializer = ApplicationSerializer(applications, many=True)
            return Response({"message": "Job applications fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No job applications found."}, status=status.HTTP_404_NOT_FOUND)
        
class JobApplicationListViewById(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        if request.user.user_role != 'recruiter':
            return Response({"detail": "Sorry, only recruiters can view job applications."}, status=status.HTTP_403_FORBIDDEN)

        try:
            application = Application.objects.get(id=id)
        except Application.DoesNotExist:
            return Response({"detail": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)
# ===================================================

class JobApplicationDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    lookup_field = 'id'
    
    def get(self, request, id):
        try:
            job_application = Application.objects.get(id=id)
        except Application.DoesNotExist:
            return Response({"detail": "Job application not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view job application."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ApplicationSerializer(job_application)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            job_application = Application.objects.get(id=id)
        except Application.DoesNotExist:
            return Response({"detail": "Job application not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can update job application."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ApplicationSerializer(job_application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job application updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            job_application = Application.objects.get(id=id)
        except Application.DoesNotExist:
            return Response({"detail": "Job application not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can delete job application."}, status=status.HTTP_403_FORBIDDEN)
        job_application.delete()
        return Response({"message": "Job application deleted successfully!"}, status=status.HTTP_200_OK)
    


# Formal Education List
# ==========================
class FormalEducationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view Language Skills."}, status=status.HTTP_403_FORBIDDEN)

        education = Formal_education.objects.filter(applicant=request.user.applicant)
        if education:
            serializer = Formal_educationSerializer(education, many=True)
            return Response({"message": "Formal Education data fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Formal Education data found."}, status=status.HTTP_404_NOT_FOUND)
            
# Formal Education Update and Delete
# ====================================
class FormalEducationDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Formal_education.objects.all()
    serializer_class = Formal_educationSerializer
    lookup_field = 'id'
    
    def get(self, request, id):
        try:
            formal_education = Formal_education.objects.get(id=id)
        except Formal_education.DoesNotExist:
            return Response({"detail": "Formal education not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view formal education."}, status=status.HTTP_403_FORBIDDEN)
        serializer = Formal_educationSerializer(formal_education)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            formal_education = Formal_education.objects.get(id=id)
        except Formal_education.DoesNotExist:
            return Response({"detail": "Formal education not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can update formal education."}, status=status.HTTP_403_FORBIDDEN)
        serializer = Formal_educationSerializer(formal_education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Formal education updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            formal_education = Formal_education.objects.get(id=id)
        except Formal_education.DoesNotExist:
            return Response({"detail": "Formal education not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can delete formal education."}, status=status.HTTP_403_FORBIDDEN)
        formal_education.delete()
        return Response({"message": "Formal education deleted successfully!"}, status=status.HTTP_200_OK)
    
# # Work Experince List
# ====================================
class WorkExperienceListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view work experience."}, status=status.HTTP_403_FORBIDDEN)
        
        experience = Work_experience.objects.filter(applicant=request.user.applicant)
        if experience:
            serializer = Work_experienceSerializer(experience, many=True)
            return Response({"message": "Work Experience fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Work Experience found."}, status=status.HTTP_404_NOT_FOUND)
        
# Work Experince Update and Delete
# ====================================
class WorkExperienceDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Work_experience.objects.all()
    serializer_class = Work_experienceSerializer
    lookup_field = 'id'
    
    def get(self, request, id):
        try:
            work_experience = Work_experience.objects.get(id=id)
        except Work_experience.DoesNotExist:
            return Response({"detail": "Work experience not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view work experience."}, status=status.HTTP_403_FORBIDDEN)
        serializer = Work_experienceSerializer(work_experience)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            work_experience = Work_experience.objects.get(id=id)
        except Work_experience.DoesNotExist:
            return Response({"detail": "Work experience not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can update work experience."}, status=status.HTTP_403_FORBIDDEN)
        serializer = Work_experienceSerializer(work_experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Work experience updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            work_experience = Work_experience.objects.get(id=id)
        except Work_experience.DoesNotExist:
            return Response({"detail": "Work experience not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can delete work experience."}, status=status.HTTP_403_FORBIDDEN)
        work_experience.delete()
        return Response({"message": "Work experience deleted successfully!"}, status=status.HTTP_200_OK)

# # Language Skills List
# ==========================
class LanguageSkillsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view Language Skills."}, status=status.HTTP_403_FORBIDDEN)

        language = Language_skills.objects.filter(applicant=request.user.applicant)
        if language:
            serializer = Language_skillsSerializer(language, many=True)
            return Response({"message": "Language Skills fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Language Skills found."}, status=status.HTTP_404_NOT_FOUND)
    
# # Language Skills update and Delete
# ===========================================
class LanguageSkillsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Language_skills.objects.all()
    serializer_class = Language_skillsSerializer
    lookup_field = 'id'
    
    def get(self, request, id):
        try:
            language_skills = Language_skills.objects.get(id=id)
        except Language_skills.DoesNotExist:
            return Response({"detail": "Language skills not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view language skills."}, status=status.HTTP_403_FORBIDDEN)
        serializer = Language_skillsSerializer(language_skills)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            language_skills = Language_skills.objects.get(id=id)
        except Language_skills.DoesNotExist:
            return Response({"detail": "Language skills not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can update language skills."}, status=status.HTTP_403_FORBIDDEN)
        serializer = Language_skillsSerializer(language_skills, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Language skills updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            language_skills = Language_skills.objects.get(id=id)
        except Language_skills.DoesNotExist:
            return Response({"detail": "Language skills not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can delete language skills."}, status=status.HTTP_403_FORBIDDEN)
        language_skills.delete()
        return Response({"message": "Language skills deleted successfully!"}, status=status.HTTP_200_OK)
    

# Applicant List
# ==========================
class ApplicantListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view Language Skills."}, status=status.HTTP_403_FORBIDDEN)

        applicant = Applicant.objects.filter(applicant=request.user.applicant)
        if applicant:
            serializer = ApplicantSerializer(applicant, many=True)
            return Response({"message": "Applicant Information fetched successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Applicant Information found."}, status=status.HTTP_404_NOT_FOUND)
        
class ApplicantDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    lookup_field = 'id'
    
    def get(self, request, id):
        try:
            applicant = Applicant.objects.get(id=id)
        except Applicant.DoesNotExist:
            return Response({"detail": "Applicant not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can view applicant profile."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            applicant = Applicant.objects.get(id=id)
        except Applicant.DoesNotExist:
            return Response({"detail": "Applicant not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can update applicant profile."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ApplicantSerializer(applicant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Applicant profile updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            applicant = Applicant.objects.get(id=id)
        except Applicant.DoesNotExist:
            return Response({"detail": "Applicant not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.user_role != 'applicant':
            return Response({"detail": "Sorry, only applicant can delete applicant profile."}, status=status.HTTP_403_FORBIDDEN)
        applicant.delete()
        return Response({"message": "Applicant profile deleted successfully!"}, status=status.HTTP_200_OK)