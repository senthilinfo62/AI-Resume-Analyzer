"""
Services for the resume analyzer application.
These handle external dependencies and business logic.
"""
import os
import uuid
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data (uncomment when needed)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


class FileService:
    """Service for handling file operations."""
    
    def __init__(self, media_root):
        self.media_root = media_root
        self.upload_dir = os.path.join(media_root, 'resumes')
        
        # Create the upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def save(self, file):
        """
        Save a file to the upload directory.
        
        Args:
            file: The file to save.
            
        Returns:
            The path to the saved file.
        """
        # Generate a unique filename
        filename = f"{uuid.uuid4()}_{file.name}"
        file_path = os.path.join(self.upload_dir, filename)
        
        # Save the file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        return file_path
    
    def extract_text(self, file_path):
        """
        Extract text from a file.
        
        Args:
            file_path: The path to the file.
            
        Returns:
            The extracted text.
        """
        # This is a simplified implementation
        # In a real application, you would use libraries like PyPDF2, docx2txt, etc.
        # based on the file type
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif file_extension == '.pdf':
            # Placeholder for PDF extraction
            # In a real app, use PyPDF2 or similar
            return "PDF text extraction placeholder"
        elif file_extension in ['.docx', '.doc']:
            # Placeholder for Word document extraction
            # In a real app, use docx2txt or similar
            return "Word document text extraction placeholder"
        else:
            return "Unsupported file format"


class ResumeAnalyzerService:
    """Service for analyzing resumes."""
    
    def __init__(self, feedback_repository):
        self.feedback_repository = feedback_repository
        
        # Initialize NLP components
        self.stopwords = nltk.corpus.stopwords.words('english') if nltk.download('stopwords') else []
        self.vectorizer = TfidfVectorizer(stop_words=self.stopwords)
        
        # Sample job descriptions for different categories
        # In a real application, these would be more comprehensive and possibly stored in a database
        self.job_descriptions = {
            'technical_skills': "Python Java JavaScript C++ SQL Database Machine Learning AI Data Science Cloud AWS Azure DevOps Docker Kubernetes Git",
            'education': "Bachelor Master PhD Degree University College School GPA Academic Scholarship",
            'experience': "Years Experience Professional Career Job Work Position Role Responsibility Team Lead Manage",
            'achievements': "Achievement Award Recognition Accomplishment Success Project Delivered Improved Increased Decreased Optimized",
            'formatting': "Format Layout Structure Organization Clear Concise Professional Resume CV"
        }
    
    def analyze(self, resume_content):
        """
        Analyze a resume and generate a score and feedback.
        
        Args:
            resume_content: The text content of the resume.
            
        Returns:
            A tuple of (score, feedback) where score is a number from 0-100
            and feedback is a dictionary of category-specific feedback.
        """
        # Calculate scores for each category
        category_scores = {}
        feedback = {}
        
        for category, description in self.job_descriptions.items():
            score, category_feedback = self._analyze_category(resume_content, description, category)
            category_scores[category] = score
            feedback[category] = category_feedback
        
        # Calculate overall score (weighted average)
        weights = {
            'technical_skills': 0.3,
            'education': 0.2,
            'experience': 0.3,
            'achievements': 0.1,
            'formatting': 0.1
        }
        
        overall_score = sum(category_scores[cat] * weights[cat] for cat in weights)
        
        # Round to nearest integer
        overall_score = round(overall_score)
        
        return overall_score, feedback
    
    def _analyze_category(self, resume_content, category_description, category_name):
        """
        Analyze a specific category of the resume.
        
        Args:
            resume_content: The text content of the resume.
            category_description: The description of the category.
            category_name: The name of the category.
            
        Returns:
            A tuple of (score, feedback) for the category.
        """
        # Vectorize the resume and category description
        documents = [resume_content, category_description]
        try:
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert similarity to a score from 0-100
            score = min(100, max(0, round(similarity * 100)))
            
            # Generate feedback based on the score
            feedback = self._generate_feedback(score, category_name)
            
            return score, feedback
        except Exception as e:
            # Handle errors gracefully
            return 50, f"Error analyzing {category_name}: {str(e)}"
    
    def _generate_feedback(self, score, category):
        """
        Generate feedback based on the score and category.
        
        Args:
            score: The score from 0-100.
            category: The category name.
            
        Returns:
            Feedback text.
        """
        if category == 'technical_skills':
            if score >= 80:
                return "Excellent technical skills section. Your skills are well-aligned with industry demands."
            elif score >= 60:
                return "Good technical skills, but consider adding more relevant technologies and frameworks."
            else:
                return "Your technical skills section needs improvement. Add more specific technologies and frameworks relevant to your target roles."
        
        elif category == 'education':
            if score >= 80:
                return "Education section is well-presented with relevant details."
            elif score >= 60:
                return "Education section is adequate, but consider adding more details about coursework or achievements."
            else:
                return "Your education section needs more details. Include degrees, institutions, graduation dates, and relevant coursework."
        
        elif category == 'experience':
            if score >= 80:
                return "Strong experience section with clear accomplishments and responsibilities."
            elif score >= 60:
                return "Good experience section, but try to quantify your achievements and use more action verbs."
            else:
                return "Your experience section needs improvement. Focus on achievements rather than just responsibilities, and use metrics where possible."
        
        elif category == 'achievements':
            if score >= 80:
                return "Excellent presentation of achievements with measurable results."
            elif score >= 60:
                return "Good achievements, but try to quantify your impact more clearly."
            else:
                return "Your achievements section needs improvement. Add specific, measurable accomplishments from your career or education."
        
        elif category == 'formatting':
            if score >= 80:
                return "Resume is well-formatted and easy to read."
            elif score >= 60:
                return "Formatting is adequate, but could be improved for better readability."
            else:
                return "Your resume formatting needs improvement. Ensure consistent spacing, fonts, and a clean, professional layout."
        
        else:
            return "No specific feedback available for this category."
