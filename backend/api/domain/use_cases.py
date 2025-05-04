"""
Use cases for the resume analyzer application.
These represent the business logic of the application.
"""
from dataclasses import dataclass

@dataclass
class JobDescription:
    """Job description entity."""
    title: str
    description: str
    company: str = ""
    location: str = ""

class ResumeAnalysisUseCase:
    """Use case for analyzing a resume using advanced AI techniques."""

    def __init__(self, resume_repository, analyzer_service):
        self.resume_repository = resume_repository
        self.analyzer_service = analyzer_service

    def execute(self, resume_id):
        """
        Analyze a resume and save the results.

        Args:
            resume_id: The ID of the resume to analyze.

        Returns:
            The analyzed resume with score and feedback.
        """
        # Get the resume from the repository
        resume = self.resume_repository.get_by_id(resume_id)

        if not resume:
            raise ValueError(f"Resume with ID {resume_id} not found")

        # Analyze the resume
        score, feedback = self.analyzer_service.analyze(resume.content)

        # Update the resume with the analysis results
        resume.score = score
        resume.feedback = feedback

        # Save the updated resume
        updated_resume = self.resume_repository.update(resume)

        return updated_resume


class ResumeUploadUseCase:
    """Use case for uploading a resume."""

    def __init__(self, resume_repository, file_service):
        self.resume_repository = resume_repository
        self.file_service = file_service

    def execute(self, user_id, file):
        """
        Upload a resume file and extract its content.

        Args:
            user_id: The ID of the user uploading the resume.
            file: The resume file to upload.

        Returns:
            The created resume entity.
        """
        # Save the file
        file_path = self.file_service.save(file)

        # Extract content from the file
        content = self.file_service.extract_text(file_path)

        # Create a new resume entity
        resume = self.resume_repository.create(
            user_id=user_id,
            file_path=file_path,
            content=content
        )

        return resume


class GetUserResumesUseCase:
    """Use case for getting all resumes for a user."""

    def __init__(self, resume_repository):
        self.resume_repository = resume_repository

    def execute(self, user_id):
        """
        Get all resumes for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of resume entities.
        """
        return self.resume_repository.get_by_user_id(user_id)


class JobComparisonUseCase:
    """Use case for comparing a resume with a job description."""

    def __init__(self, resume_repository, analyzer_service):
        self.resume_repository = resume_repository
        self.analyzer_service = analyzer_service

    def execute(self, resume_id, job_description):
        """
        Compare a resume with a job description.

        Args:
            resume_id: The ID of the resume to compare.
            job_description: The job description to compare with.

        Returns:
            Dictionary with match results.
        """
        # Get the resume from the repository
        resume = self.resume_repository.get_by_id(resume_id)

        if not resume:
            raise ValueError(f"Resume with ID {resume_id} not found")

        # Compare the resume with the job description
        match_results = self.analyzer_service.compare_with_job(
            resume.content,
            job_description.description
        )

        return match_results
