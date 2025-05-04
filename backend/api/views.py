from django.conf import settings
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Resume, Feedback
from .serializers import ResumeSerializer, FeedbackSerializer, ResumeUploadSerializer
from .adapters.services import FileService, ResumeAnalyzerService
from .adapters.repositories import ResumeRepository, FeedbackRepository
from .domain.use_cases import (
    ResumeUploadUseCase,
    ResumeAnalysisUseCase,
    GetUserResumesUseCase,
    JobComparisonUseCase,
    JobDescription
)


class ResumeViewSet(viewsets.ModelViewSet):
    """ViewSet for Resume model."""

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """Filter resumes by the current user."""
        return Resume.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], serializer_class=ResumeUploadSerializer)
    def upload(self, request):
        """Upload a new resume."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Initialize services and repositories
        file_service = FileService(settings.MEDIA_ROOT)
        resume_repository = ResumeRepository(Resume)

        # Initialize use case
        upload_use_case = ResumeUploadUseCase(resume_repository, file_service)

        # Execute use case
        resume = upload_use_case.execute(request.user.id, serializer.validated_data['file'])

        # Return response
        return Response(
            ResumeSerializer(Resume.objects.get(id=resume.id)).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """Analyze a resume."""
        # Initialize services and repositories
        feedback_repository = FeedbackRepository(Feedback)
        analyzer_service = ResumeAnalyzerService(feedback_repository)
        resume_repository = ResumeRepository(Resume)

        # Check if job description is provided
        job_description = None
        if 'job_title' in request.data and 'job_description' in request.data:
            job_description = JobDescription(
                title=request.data.get('job_title', ''),
                description=request.data.get('job_description', ''),
                company=request.data.get('company', ''),
                location=request.data.get('location', '')
            )

        # Initialize use case
        analysis_use_case = ResumeAnalysisUseCase(resume_repository, analyzer_service)

        try:
            # Execute use case
            if job_description:
                # If job description is provided, analyze with job comparison
                resume = self.analyze_with_job(pk, job_description, resume_repository, analyzer_service, feedback_repository)
            else:
                # Regular analysis without job description
                resume = analysis_use_case.execute(pk)

                # Save detailed feedback for main categories
                main_categories = ['technical_skills', 'education', 'experience', 'achievements', 'formatting']
                for category in main_categories:
                    if category in resume.feedback:
                        feedback_repository.create(
                            resume_id=resume.id,
                            category=category,
                            content=resume.feedback[category],
                            score=resume.feedback.get('category_scores', {}).get(category, resume.score)
                        )

            # Return response
            return Response(
                ResumeSerializer(Resume.objects.get(id=resume.id)).data,
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def analyze_with_job(self, resume_id, job_description, resume_repository, analyzer_service, feedback_repository):
        """Analyze a resume with job description comparison."""
        # Get the resume
        resume = resume_repository.get_by_id(resume_id)

        if not resume:
            raise ValueError(f"Resume with ID {resume_id} not found")

        # Analyze the resume with job description
        score, feedback = analyzer_service.analyze(resume.content, job_description.description)

        # Update the resume with the analysis results
        resume.score = score
        resume.feedback = feedback

        # Save the updated resume
        updated_resume = resume_repository.update(resume)

        # Save detailed feedback for main categories
        main_categories = ['technical_skills', 'education', 'experience', 'achievements', 'formatting']
        for category in main_categories:
            if category in resume.feedback:
                feedback_repository.create(
                    resume_id=resume.id,
                    category=category,
                    content=resume.feedback[category],
                    score=resume.feedback.get('category_scores', {}).get(category, resume.score)
                )

        return updated_resume

    @action(detail=True, methods=['post'])
    def compare_job(self, request, pk=None):
        """Compare a resume with a job description."""
        # Validate input
        if 'job_title' not in request.data or 'job_description' not in request.data:
            return Response(
                {'error': 'Job title and description are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create job description object
        job_description = JobDescription(
            title=request.data.get('job_title', ''),
            description=request.data.get('job_description', ''),
            company=request.data.get('company', ''),
            location=request.data.get('location', '')
        )

        # Initialize services and repositories
        feedback_repository = FeedbackRepository(Feedback)
        analyzer_service = ResumeAnalyzerService(feedback_repository)
        resume_repository = ResumeRepository(Resume)

        # Initialize use case
        job_comparison_use_case = JobComparisonUseCase(resume_repository, analyzer_service)

        try:
            # Execute use case
            match_results = job_comparison_use_case.execute(pk, job_description)

            # Return response
            return Response(match_results, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FeedbackViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Feedback model."""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter feedback by the current user's resumes."""
        return Feedback.objects.filter(resume__user=self.request.user)
