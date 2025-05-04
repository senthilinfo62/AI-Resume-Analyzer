"""
Services for the resume analyzer application.
These handle external dependencies and business logic.
"""
import os
import uuid
from ..ai.resume_analyzer import AdvancedResumeAnalyzer


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
    """Service for analyzing resumes using advanced NLP techniques."""

    def __init__(self, feedback_repository):
        self.feedback_repository = feedback_repository

        # Initialize the advanced resume analyzer
        self.analyzer = AdvancedResumeAnalyzer()

    def analyze(self, resume_content):
        """
        Analyze a resume and generate a score and feedback.

        Args:
            resume_content: The text content of the resume.

        Returns:
            A tuple of (score, feedback) where score is a number from 0-100
            and feedback is a dictionary of category-specific feedback.
        """
        try:
            # Use the advanced analyzer to analyze the resume
            results = self.analyzer.analyze_resume(resume_content)

            # Extract the overall score and feedback
            overall_score = results['score']
            feedback = results['feedback']

            # Add additional analysis results to the feedback
            feedback['improvement_suggestions'] = results['improvement_suggestions']
            feedback['key_strengths'] = results['key_strengths']
            feedback['job_role'] = results['job_role']
            feedback['job_role_confidence'] = results['job_role_confidence']
            feedback['keywords'] = results['keywords']

            return overall_score, feedback
        except Exception as e:
            # Handle errors gracefully
            print(f"Error analyzing resume: {str(e)}")

            # Provide default values in case of error
            default_feedback = {
                'technical_skills': "Unable to analyze technical skills due to an error.",
                'education': "Unable to analyze education due to an error.",
                'experience': "Unable to analyze experience due to an error.",
                'achievements': "Unable to analyze achievements due to an error.",
                'formatting': "Unable to analyze formatting due to an error.",
                'improvement_suggestions': ["Ensure your resume is in a standard format"],
                'key_strengths': ["Unable to identify key strengths due to an error"],
                'job_role': "Unknown",
                'job_role_confidence': 0,
                'keywords': []
            }

            return 50, default_feedback
