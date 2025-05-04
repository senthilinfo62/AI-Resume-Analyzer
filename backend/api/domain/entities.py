"""
Domain entities for the resume analyzer application.
These are the core business objects that are independent of any framework.
"""

class Resume:
    """Resume entity representing a user's resume."""
    
    def __init__(self, id=None, user_id=None, file_path=None, content=None, 
                 score=None, feedback=None, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.file_path = file_path
        self.content = content
        self.score = score
        self.feedback = feedback
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self):
        return f"Resume(id={self.id}, user_id={self.user_id}, score={self.score})"


class User:
    """User entity representing a user of the application."""
    
    def __init__(self, id=None, username=None, email=None, password=None, 
                 first_name=None, last_name=None, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Feedback:
    """Feedback entity representing feedback for a resume."""
    
    def __init__(self, id=None, resume_id=None, category=None, content=None, 
                 score=None, created_at=None):
        self.id = id
        self.resume_id = resume_id
        self.category = category
        self.content = content
        self.score = score
        self.created_at = created_at
    
    def __str__(self):
        return f"Feedback(id={self.id}, resume_id={self.resume_id}, category={self.category}, score={self.score})"
