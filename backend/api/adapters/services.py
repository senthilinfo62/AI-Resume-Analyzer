"""
Services for the resume analyzer application.
These handle external dependencies and business logic.
"""
import os
import uuid
from ..ai.resume_analyzer import AdvancedResumeAnalyzer
from ..ai.job_matcher import JobMatcher


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

        # Initialize the advanced resume analyzer and job matcher
        self.analyzer = AdvancedResumeAnalyzer()
        self.job_matcher = JobMatcher()

    def analyze(self, resume_content, job_description=None):
        """
        Analyze a resume and generate a score and feedback.

        Args:
            resume_content: The text content of the resume.
            job_description: Optional job description to compare with the resume.

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

            # If job description is provided, compare with resume
            if job_description:
                match_results = self.job_matcher.calculate_match_score(resume_content, job_description)
                job_suggestions = self.job_matcher.generate_improvement_suggestions(match_results)

                # Add job match results to feedback
                feedback['job_match'] = {
                    'overall_match_score': match_results['overall_match_score'],
                    'similarity_score': match_results['similarity_score'],
                    'skill_match_scores': match_results['skill_match_scores'],
                    'missing_skills': match_results['missing_skills'],
                    'matched_skills': match_results['matched_skills'],
                    'job_specific_suggestions': job_suggestions
                }

                # Add job-specific suggestions to improvement suggestions
                feedback['improvement_suggestions'].extend(job_suggestions)

                # Remove duplicates from improvement suggestions
                feedback['improvement_suggestions'] = list(set(feedback['improvement_suggestions']))

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

    def compare_with_job(self, resume_content, job_description):
        """
        Compare a resume with a job description.

        Args:
            resume_content: The text content of the resume.
            job_description: The text content of the job description.

        Returns:
            Dictionary with match results.
        """
        try:
            # Calculate match score
            match_results = self.job_matcher.calculate_match_score(resume_content, job_description)

            # Generate improvement suggestions
            job_suggestions = self.job_matcher.generate_improvement_suggestions(match_results)

            # Add suggestions to results
            match_results['job_specific_suggestions'] = job_suggestions

            return match_results
        except Exception as e:
            # Handle errors gracefully
            print(f"Error comparing resume with job description: {str(e)}")

            # Provide default values in case of error
            default_results = {
                'overall_match_score': 50,
                'similarity_score': 50,
                'skill_match_scores': {'technical': 50, 'soft': 50, 'domain': 50},
                'missing_skills': {'technical': [], 'soft': [], 'domain': []},
                'matched_skills': {'technical': [], 'soft': [], 'domain': []},
                'job_specific_suggestions': ["Unable to generate job-specific suggestions due to an error."]
            }

            return default_results
