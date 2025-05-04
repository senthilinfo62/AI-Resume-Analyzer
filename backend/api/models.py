from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Resume(models.Model):
    """Model for storing resume information."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file_path = models.CharField(max_length=255)
    content = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    feedback = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume for {self.user.username} (ID: {self.id})"


class Feedback(models.Model):
    """Model for storing detailed feedback for resumes."""

    CATEGORY_CHOICES = [
        ('technical_skills', 'Technical Skills'),
        ('education', 'Education'),
        ('experience', 'Experience'),
        ('achievements', 'Achievements'),
        ('formatting', 'Formatting'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='detailed_feedback')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('resume', 'category')

    def __str__(self):
        return f"Feedback for {self.resume.user.username}'s resume - {self.category}"
