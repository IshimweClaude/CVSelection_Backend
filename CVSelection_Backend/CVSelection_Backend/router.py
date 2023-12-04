from JobApplication.viewsets import JobViewset, Formal_educationViewset, Work_experienceViewset, Language_skillsViewset, ApplicationViewset  
from rest_framework import routers                            # import routers from rest_framework

router =routers.DefaultRouter()                              # create a router object

router.register('job',JobViewset)
# router.register('country',CountryViewset)
router.register('education',Formal_educationViewset)
router.register('experience',Work_experienceViewset)
router.register('language',Language_skillsViewset)
router.register('application',ApplicationViewset)  



