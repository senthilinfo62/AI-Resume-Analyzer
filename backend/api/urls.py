from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, FeedbackViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'resumes', ResumeViewSet)
router.register(r'feedback', FeedbackViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
