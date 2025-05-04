from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Resume, Feedback


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for Feedback model."""
    
    class Meta:
        model = Feedback
        fields = ['id', 'resume', 'category', 'content', 'score', 'created_at']
        read_only_fields = ['id', 'created_at']


class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume model."""
    
    user = UserSerializer(read_only=True)
    detailed_feedback = FeedbackSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resume
        fields = ['id', 'user', 'file_path', 'content', 'score', 'feedback', 
                  'detailed_feedback', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'file_path', 'content', 'score', 
                           'feedback', 'created_at', 'updated_at']


class ResumeUploadSerializer(serializers.Serializer):
    """Serializer for resume upload."""
    
    file = serializers.FileField()
    
    def validate_file(self, value):
        """Validate the uploaded file."""
        # Check file size (max 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 5MB")
        
        # Check file extension
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_extension = value.name.lower().split('.')[-1]
        
        if f'.{file_extension}' not in allowed_extensions:
            raise serializers.ValidationError(
                f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
            )
        
        return value
