"""
Job description matcher for resume analysis.
"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatcher:
    """Job description matcher for resume analysis."""

    def __init__(self):
        """Initialize the job matcher with required NLP components."""
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Skills categories for matching
        self.skill_categories = {
            'technical': [
                'programming', 'coding', 'software', 'development', 'engineering', 
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go',
                'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 
                'database', 'sql', 'mysql', 'postgresql', 'mongodb', 'nosql',
                'aws', 'azure', 'cloud', 'docker', 'kubernetes', 'devops',
                'git', 'github', 'gitlab', 'ci/cd', 'jenkins', 'testing'
            ],
            'soft': [
                'communication', 'teamwork', 'leadership', 'problem-solving', 
                'critical thinking', 'time management', 'organization', 'adaptability',
                'creativity', 'collaboration', 'interpersonal', 'presentation',
                'negotiation', 'conflict resolution', 'decision making', 'flexibility'
            ],
            'domain': [
                'finance', 'healthcare', 'education', 'retail', 'manufacturing',
                'marketing', 'sales', 'customer service', 'human resources', 'operations',
                'project management', 'product management', 'data analysis', 'research',
                'consulting', 'legal', 'compliance', 'security', 'quality assurance'
            ]
        }

    def preprocess_text(self, text):
        """
        Preprocess text by tokenizing, removing stopwords, and lemmatizing.
        
        Args:
            text: The text to preprocess.
            
        Returns:
            Preprocessed text.
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stopwords]
        
        # Join tokens back into text
        preprocessed_text = ' '.join(tokens)
        
        return preprocessed_text

    def extract_skills(self, text):
        """
        Extract skills from text and categorize them.
        
        Args:
            text: The text to extract skills from.
            
        Returns:
            Dictionary of categorized skills.
        """
        preprocessed_text = self.preprocess_text(text)
        tokens = preprocessed_text.split()
        
        categorized_skills = {
            'technical': [],
            'soft': [],
            'domain': []
        }
        
        for token in tokens:
            for category, skills in self.skill_categories.items():
                if token in skills:
                    if token not in categorized_skills[category]:
                        categorized_skills[category].append(token)
        
        return categorized_skills

    def calculate_match_score(self, resume_text, job_description):
        """
        Calculate the match score between a resume and job description.
        
        Args:
            resume_text: The text content of the resume.
            job_description: The text content of the job description.
            
        Returns:
            Dictionary with match scores and details.
        """
        # Preprocess texts
        preprocessed_resume = self.preprocess_text(resume_text)
        preprocessed_job = self.preprocess_text(job_description)
        
        # Calculate overall similarity
        documents = [preprocessed_resume, preprocessed_job]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        overall_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Extract skills
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)
        
        # Calculate skill match scores
        skill_match_scores = {}
        missing_skills = {}
        
        for category in self.skill_categories.keys():
            resume_category_skills = set(resume_skills[category])
            job_category_skills = set(job_skills[category])
            
            # Calculate match score for this category
            if len(job_category_skills) > 0:
                matched_skills = resume_category_skills.intersection(job_category_skills)
                skill_match_scores[category] = len(matched_skills) / len(job_category_skills) * 100
                missing_skills[category] = list(job_category_skills - resume_category_skills)
            else:
                skill_match_scores[category] = 100
                missing_skills[category] = []
        
        # Calculate weighted overall score
        weights = {
            'technical': 0.6,
            'soft': 0.2,
            'domain': 0.2
        }
        
        weighted_score = sum(skill_match_scores[category] * weights[category] 
                            for category in weights.keys())
        
        # Combine with TF-IDF similarity for final score
        final_score = 0.7 * weighted_score + 0.3 * (overall_similarity * 100)
        final_score = min(100, max(0, round(final_score)))
        
        # Prepare result
        result = {
            'overall_match_score': final_score,
            'similarity_score': round(overall_similarity * 100),
            'skill_match_scores': {k: round(v) for k, v in skill_match_scores.items()},
            'missing_skills': missing_skills,
            'matched_skills': {
                category: list(set(resume_skills[category]).intersection(set(job_skills[category])))
                for category in self.skill_categories.keys()
            }
        }
        
        return result

    def generate_improvement_suggestions(self, match_result):
        """
        Generate improvement suggestions based on match results.
        
        Args:
            match_result: The result from calculate_match_score.
            
        Returns:
            List of improvement suggestions.
        """
        suggestions = []
        
        # Add suggestions based on missing skills
        for category, skills in match_result['missing_skills'].items():
            if skills:
                if category == 'technical':
                    suggestions.append(f"Add these technical skills to your resume: {', '.join(skills[:5])}")
                    if len(skills) > 5:
                        suggestions.append(f"Consider learning these additional technical skills: {', '.join(skills[5:10])}")
                elif category == 'soft':
                    suggestions.append(f"Highlight these soft skills in your resume: {', '.join(skills)}")
                elif category == 'domain':
                    suggestions.append(f"Add domain knowledge in: {', '.join(skills)}")
        
        # Add general suggestions based on match score
        overall_score = match_result['overall_match_score']
        
        if overall_score < 50:
            suggestions.append("Your resume needs significant tailoring for this job description")
            suggestions.append("Consider a complete resume rewrite focusing on the required skills")
        elif overall_score < 70:
            suggestions.append("Tailor your resume more specifically to this job description")
            suggestions.append("Reorganize your skills section to highlight relevant experience")
        else:
            suggestions.append("Your resume is well-matched to this job description")
            suggestions.append("Consider emphasizing your most relevant achievements more prominently")
        
        return suggestions
