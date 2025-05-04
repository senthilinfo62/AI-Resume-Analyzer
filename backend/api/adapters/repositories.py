"""
Repositories for the resume analyzer application.
These handle data access and persistence.
"""
from api.domain.entities import Resume, User, Feedback


class ResumeRepository:
    """Repository for Resume entities."""
    
    def __init__(self, resume_model):
        self.resume_model = resume_model
    
    def create(self, user_id, file_path, content):
        """
        Create a new resume.
        
        Args:
            user_id: The ID of the user who owns the resume.
            file_path: The path to the resume file.
            content: The extracted text content of the resume.
            
        Returns:
            A Resume entity.
        """
        resume_obj = self.resume_model.objects.create(
            user_id=user_id,
            file_path=file_path,
            content=content
        )
        
        return self._to_entity(resume_obj)
    
    def get_by_id(self, resume_id):
        """
        Get a resume by ID.
        
        Args:
            resume_id: The ID of the resume.
            
        Returns:
            A Resume entity or None if not found.
        """
        try:
            resume_obj = self.resume_model.objects.get(id=resume_id)
            return self._to_entity(resume_obj)
        except self.resume_model.DoesNotExist:
            return None
    
    def get_by_user_id(self, user_id):
        """
        Get all resumes for a user.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            A list of Resume entities.
        """
        resume_objs = self.resume_model.objects.filter(user_id=user_id)
        return [self._to_entity(obj) for obj in resume_objs]
    
    def update(self, resume):
        """
        Update a resume.
        
        Args:
            resume: The Resume entity to update.
            
        Returns:
            The updated Resume entity.
        """
        resume_obj = self.resume_model.objects.get(id=resume.id)
        
        # Update fields
        if resume.score is not None:
            resume_obj.score = resume.score
        if resume.feedback is not None:
            resume_obj.feedback = resume.feedback
        
        resume_obj.save()
        
        return self._to_entity(resume_obj)
    
    def delete(self, resume_id):
        """
        Delete a resume.
        
        Args:
            resume_id: The ID of the resume to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            resume_obj = self.resume_model.objects.get(id=resume_id)
            resume_obj.delete()
            return True
        except self.resume_model.DoesNotExist:
            return False
    
    def _to_entity(self, resume_obj):
        """
        Convert a resume model object to a Resume entity.
        
        Args:
            resume_obj: The resume model object.
            
        Returns:
            A Resume entity.
        """
        return Resume(
            id=resume_obj.id,
            user_id=resume_obj.user_id,
            file_path=resume_obj.file_path,
            content=resume_obj.content,
            score=resume_obj.score,
            feedback=resume_obj.feedback,
            created_at=resume_obj.created_at,
            updated_at=resume_obj.updated_at
        )


class FeedbackRepository:
    """Repository for Feedback entities."""
    
    def __init__(self, feedback_model):
        self.feedback_model = feedback_model
    
    def create(self, resume_id, category, content, score):
        """
        Create a new feedback.
        
        Args:
            resume_id: The ID of the resume.
            category: The category of the feedback.
            content: The content of the feedback.
            score: The score for this feedback category.
            
        Returns:
            A Feedback entity.
        """
        feedback_obj = self.feedback_model.objects.create(
            resume_id=resume_id,
            category=category,
            content=content,
            score=score
        )
        
        return self._to_entity(feedback_obj)
    
    def get_by_resume_id(self, resume_id):
        """
        Get all feedback for a resume.
        
        Args:
            resume_id: The ID of the resume.
            
        Returns:
            A list of Feedback entities.
        """
        feedback_objs = self.feedback_model.objects.filter(resume_id=resume_id)
        return [self._to_entity(obj) for obj in feedback_objs]
    
    def _to_entity(self, feedback_obj):
        """
        Convert a feedback model object to a Feedback entity.
        
        Args:
            feedback_obj: The feedback model object.
            
        Returns:
            A Feedback entity.
        """
        return Feedback(
            id=feedback_obj.id,
            resume_id=feedback_obj.resume_id,
            category=feedback_obj.category,
            content=feedback_obj.content,
            score=feedback_obj.score,
            created_at=feedback_obj.created_at
        )
