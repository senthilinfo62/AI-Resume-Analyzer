"""
Advanced resume analyzer using NLP and machine learning.
"""
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


class AdvancedResumeAnalyzer:
    """Advanced resume analyzer using NLP and machine learning."""

    def __init__(self):
        """Initialize the analyzer with required NLP components."""
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Job descriptions for different categories
        self.job_descriptions = {
            'technical_skills': """
                Programming Languages: Python Java JavaScript TypeScript C++ C# PHP Ruby Go Rust Swift Kotlin
                Web Development: HTML CSS React Angular Vue.js Node.js Express.js Django Flask Spring Boot
                Data Science: Machine Learning Deep Learning TensorFlow PyTorch scikit-learn Pandas NumPy
                Database: SQL MySQL PostgreSQL MongoDB Redis Cassandra Oracle
                Cloud: AWS Azure Google Cloud Kubernetes Docker Terraform
                DevOps: CI/CD Jenkins GitHub Actions Travis CI CircleCI
                Mobile: iOS Android React Native Flutter
                Tools: Git GitHub GitLab Jira Confluence Slack
            """,
            'education': """
                Degree Bachelor Master PhD MBA Associate Diploma Certificate
                University College School Institute Academy
                GPA Academic Honors Dean's List Cum Laude Magna Cum Laude Summa Cum Laude
                Scholarship Fellowship Grant Award
                Major Minor Concentration Specialization
                Coursework Projects Research Thesis Dissertation
                Graduated Completed Earned Received
            """,
            'experience': """
                Years Experience Professional Career Job Work Position Role
                Responsibility Duties Tasks Achievements Accomplishments Results
                Team Lead Manage Supervise Coordinate Collaborate
                Project Develop Implement Design Create Build Maintain
                Improve Enhance Optimize Streamline Increase Decrease
                Client Customer Stakeholder User
                Business Strategy Objective Goal Target Metric
                Problem Solution Challenge Opportunity Initiative
            """,
            'achievements': """
                Achievement Award Recognition Accomplishment Success
                Improved Increased Decreased Reduced Enhanced Optimized
                Saved Generated Delivered Launched Implemented
                Led Managed Supervised Coordinated Collaborated
                Exceeded Target Goal Objective Metric KPI
                Innovation Creative Solution Approach Method
                Impact Result Outcome Effect Benefit Value
                Recognized Awarded Honored Commended Praised
            """,
            'formatting': """
                Format Layout Structure Organization Design
                Clear Concise Consistent Professional Readable
                Bullet Points Sections Headings Subheadings
                Font Size Spacing Margin Alignment
                Resume CV Curriculum Vitae
                One Page Two Page Length
                Contact Information Header Footer
                Summary Profile Objective Statement
                Keywords ATS Applicant Tracking System
            """
        }
        
        # Keywords for different job roles
        self.job_role_keywords = {
            'software_engineer': """
                Software Engineer Developer Programmer Coder Full-stack Backend Frontend
                Python Java JavaScript TypeScript C++ C# PHP Ruby Go
                React Angular Vue.js Node.js Express.js Django Flask Spring Boot
                Git GitHub GitLab Version Control
                Agile Scrum Kanban Jira
                API REST GraphQL Microservices
                Testing Unit Integration Automated
                Database SQL NoSQL MySQL PostgreSQL MongoDB
                Cloud AWS Azure Google Cloud
                DevOps CI/CD Docker Kubernetes
            """,
            'data_scientist': """
                Data Scientist Analyst Machine Learning Engineer AI
                Python R SQL
                Machine Learning Deep Learning Neural Networks
                TensorFlow PyTorch Keras scikit-learn
                Data Analysis Data Visualization Data Mining
                Statistics Probability Regression Classification Clustering
                Pandas NumPy SciPy Matplotlib Seaborn
                Big Data Hadoop Spark
                A/B Testing Hypothesis Testing
                NLP Computer Vision Time Series
            """,
            'product_manager': """
                Product Manager Product Owner
                Product Development Product Strategy Product Roadmap
                User Experience UX UI Design
                Market Research Competitive Analysis
                Customer Feedback User Testing
                Agile Scrum Kanban
                Stakeholder Management
                Business Requirements Technical Requirements
                KPIs Metrics Analytics
                Go-to-market Launch Strategy
                Cross-functional Teams
                Prioritization Backlog Management
            """,
            'marketing': """
                Marketing Digital Marketing Content Marketing Social Media Marketing
                SEO SEM PPC Google Ads Facebook Ads
                Content Strategy Content Creation
                Social Media Management
                Email Marketing Campaigns
                Analytics Google Analytics
                CRM Customer Relationship Management
                Brand Management Brand Strategy
                Market Research Competitive Analysis
                Lead Generation Conversion Rate Optimization
                Marketing Automation
            """,
            'finance': """
                Finance Financial Accounting Accountant
                Financial Analysis Financial Reporting Financial Planning
                Budgeting Forecasting Modeling
                Excel VBA PowerPoint
                Profit Loss Balance Sheet Cash Flow
                Audit Tax Compliance
                Risk Management
                Investment Banking Valuation
                CPA CFA MBA
                SAP Oracle Quickbooks
            """
        }
        
        # Common resume improvement suggestions
        self.improvement_suggestions = [
            "Add measurable achievements with specific metrics",
            "Include relevant keywords for ATS optimization",
            "Organize skills by proficiency level",
            "Use strong action verbs to begin bullet points",
            "Ensure consistent formatting throughout",
            "Quantify achievements with numbers and percentages",
            "Tailor your resume to the specific job description",
            "Remove outdated or irrelevant experience",
            "Add a concise professional summary",
            "Include relevant certifications and training",
            "Optimize your LinkedIn profile and add the URL",
            "Use industry-specific terminology",
            "Focus on accomplishments rather than responsibilities",
            "Eliminate personal pronouns (I, me, my)",
            "Keep resume to 1-2 pages maximum",
            "Use a clean, professional design",
            "Proofread for grammar and spelling errors",
            "Include relevant projects with measurable outcomes",
            "Add technical skills section with proficiency levels",
            "Use reverse chronological order for experience"
        ]

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

    def extract_keywords(self, text, top_n=20):
        """
        Extract the most important keywords from text.
        
        Args:
            text: The text to extract keywords from.
            top_n: The number of top keywords to extract.
            
        Returns:
            List of top keywords.
        """
        # Preprocess text
        preprocessed_text = self.preprocess_text(text)
        
        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer(max_features=100)
        
        try:
            # Fit and transform the text
            tfidf_matrix = vectorizer.fit_transform([preprocessed_text])
            
            # Get feature names
            feature_names = vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Create a dictionary of feature names and scores
            word_scores = {feature_names[i]: tfidf_scores[i] for i in range(len(feature_names))}
            
            # Sort by score and get top_n
            top_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            return [keyword for keyword, score in top_keywords]
        except:
            # Fallback if vectorization fails
            words = preprocessed_text.split()
            word_freq = {}
            for word in words:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
            
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
            return [keyword for keyword, freq in top_keywords]

    def identify_job_role(self, resume_text):
        """
        Identify the most likely job role based on resume content.
        
        Args:
            resume_text: The text content of the resume.
            
        Returns:
            The most likely job role and similarity score.
        """
        # Preprocess resume text
        preprocessed_resume = self.preprocess_text(resume_text)
        
        # Calculate similarity with each job role
        similarities = {}
        
        for role, keywords in self.job_role_keywords.items():
            preprocessed_keywords = self.preprocess_text(keywords)
            
            # Vectorize
            documents = [preprocessed_resume, preprocessed_keywords]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            similarities[role] = similarity
        
        # Get the role with highest similarity
        best_role = max(similarities.items(), key=lambda x: x[1])
        
        return best_role[0], best_role[1]

    def analyze_category(self, resume_text, category):
        """
        Analyze a specific category of the resume.
        
        Args:
            resume_text: The text content of the resume.
            category: The category to analyze.
            
        Returns:
            A tuple of (score, feedback) for the category.
        """
        # Preprocess resume text
        preprocessed_resume = self.preprocess_text(resume_text)
        
        # Get category description
        category_description = self.job_descriptions.get(category, "")
        preprocessed_category = self.preprocess_text(category_description)
        
        # Vectorize
        documents = [preprocessed_resume, preprocessed_category]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        
        # Calculate similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert similarity to a score from 0-100
        score = min(100, max(0, round(similarity * 100)))
        
        # Generate feedback
        feedback = self.generate_feedback(score, category, resume_text)
        
        return score, feedback

    def generate_feedback(self, score, category, resume_text):
        """
        Generate detailed feedback based on the score and category.
        
        Args:
            score: The score from 0-100.
            category: The category name.
            resume_text: The text content of the resume.
            
        Returns:
            Detailed feedback text.
        """
        # Extract keywords from the resume for this category
        category_keywords = self.extract_keywords(resume_text, top_n=10)
        keywords_str = ", ".join(category_keywords[:5])
        
        if category == 'technical_skills':
            if score >= 80:
                return f"Your technical skills section is strong, with good emphasis on {keywords_str}. Consider organizing them by proficiency level. Add more details about your expertise in specific technologies. Consider adding relevant certifications to strengthen this section."
            elif score >= 60:
                return f"Your technical skills section is adequate, highlighting {keywords_str}. However, you should add more in-demand technologies and frameworks. Group skills by categories (e.g., programming languages, frameworks, tools) and indicate proficiency levels."
            else:
                return f"Your technical skills section needs significant improvement. While you mention {keywords_str}, you should add more specific technologies and frameworks relevant to your target roles. Include programming languages, frameworks, tools, and platforms with proficiency levels."
        
        elif category == 'education':
            if score >= 80:
                return f"Education section is well-structured, highlighting {keywords_str}. Include GPA if it's above 3.5. Consider adding relevant coursework that aligns with your target positions. Highlight any academic achievements or leadership roles."
            elif score >= 60:
                return f"Your education section is adequate, mentioning {keywords_str}. Add more details about relevant coursework, academic projects, and achievements. Include GPA if it's strong, and highlight any scholarships or honors."
            else:
                return f"Your education section needs improvement. While you mention {keywords_str}, you should provide more structure and details. Include degree names, institutions, graduation dates, GPA (if above 3.0), relevant coursework, and academic achievements."
        
        elif category == 'experience':
            if score >= 80:
                return f"Your work experience is impressive, highlighting {keywords_str}. Use more action verbs and quantify your achievements with metrics. For example, 'Increased website performance by 40%' instead of 'Improved website performance'. Focus on outcomes rather than just responsibilities."
            elif score >= 60:
                return f"Your experience section is adequate, mentioning {keywords_str}. However, you should use stronger action verbs to begin each bullet point and quantify your achievements where possible. Focus more on what you accomplished rather than just listing responsibilities."
            else:
                return f"Your experience section needs significant improvement. While you mention {keywords_str}, your descriptions lack impact. Use the STAR method (Situation, Task, Action, Result) to structure your bullet points. Begin with strong action verbs and quantify achievements with specific metrics."
        
        elif category == 'achievements':
            if score >= 80:
                return f"Good list of achievements, mentioning {keywords_str}, but they could be more impactful. Quantify results where possible and connect them to business outcomes. Consider adding awards, recognitions, or publications if applicable."
            elif score >= 60:
                return f"Your achievements section is present but needs enhancement. While you mention {keywords_str}, try to quantify your accomplishments with specific metrics and highlight the impact on the organization. Add any awards, certifications, or recognitions."
            else:
                return f"Your achievements section is weak or missing. Add specific accomplishments from your career or education, quantified with metrics where possible. Include awards, recognitions, certifications, and other notable achievements that demonstrate your value."
        
        elif category == 'formatting':
            if score >= 80:
                return f"The resume layout is clean, with good use of {keywords_str}, but consider using a more modern template. Ensure consistent spacing and alignment throughout. Use bullet points for better readability and keep bullet points to 1-2 lines each."
            elif score >= 60:
                return f"Your resume formatting is adequate but could be improved. While you use {keywords_str}, ensure consistent fonts, spacing, and alignment throughout. Use bullet points instead of paragraphs for experience and achievements. Consider a cleaner, more modern template."
            else:
                return f"Your resume formatting needs significant improvement. Create a clean, professional layout with consistent fonts, spacing, and alignment. Use clear section headings, bullet points for readability, and ensure the document is ATS-friendly. Limit to 1-2 pages maximum."
        
        else:
            return "No specific feedback available for this category."

    def get_improvement_suggestions(self, resume_text, scores):
        """
        Generate personalized improvement suggestions based on resume content and scores.
        
        Args:
            resume_text: The text content of the resume.
            scores: Dictionary of category scores.
            
        Returns:
            List of improvement suggestions.
        """
        suggestions = []
        
        # Add category-specific suggestions based on scores
        for category, score in scores.items():
            if score < 70:
                if category == 'technical_skills':
                    suggestions.append("Add more specific technical skills relevant to your target role")
                    suggestions.append("Organize skills by proficiency level (e.g., Expert, Proficient, Familiar)")
                elif category == 'education':
                    suggestions.append("Include more details about relevant coursework and academic achievements")
                    suggestions.append("Add GPA if it's above 3.0")
                elif category == 'experience':
                    suggestions.append("Use strong action verbs to begin each bullet point")
                    suggestions.append("Quantify achievements with specific metrics and results")
                elif category == 'achievements':
                    suggestions.append("Add more measurable achievements with specific metrics")
                    suggestions.append("Include awards, certifications, or other recognitions")
                elif category == 'formatting':
                    suggestions.append("Improve formatting with consistent spacing and alignment")
                    suggestions.append("Use a clean, professional template with clear section headings")
        
        # Add general suggestions
        general_suggestions = random.sample(self.improvement_suggestions, min(5, len(self.improvement_suggestions)))
        suggestions.extend(general_suggestions)
        
        # Remove duplicates and limit to 10 suggestions
        unique_suggestions = list(set(suggestions))
        return unique_suggestions[:10]

    def identify_key_strengths(self, resume_text, scores):
        """
        Identify key strengths based on resume content and scores.
        
        Args:
            resume_text: The text content of the resume.
            scores: Dictionary of category scores.
            
        Returns:
            List of key strengths.
        """
        strengths = []
        
        # Add category-specific strengths based on high scores
        for category, score in scores.items():
            if score >= 75:
                if category == 'technical_skills':
                    strengths.append("Strong technical skill set")
                    keywords = self.extract_keywords(resume_text, top_n=3)
                    if keywords:
                        strengths.append(f"Proficiency in {', '.join(keywords)}")
                elif category == 'education':
                    strengths.append("Strong educational background")
                elif category == 'experience':
                    strengths.append("Solid professional experience")
                    strengths.append("Clear demonstration of career progression")
                elif category == 'achievements':
                    strengths.append("Impressive achievements with measurable results")
                elif category == 'formatting':
                    strengths.append("Well-organized and professionally formatted resume")
        
        # Identify job role and add as strength if confidence is high
        job_role, confidence = self.identify_job_role(resume_text)
        if confidence > 0.5:
            role_name = job_role.replace('_', ' ').title()
            strengths.append(f"Strong alignment with {role_name} positions")
        
        # Add general strengths based on keyword analysis
        keywords = self.extract_keywords(resume_text, top_n=10)
        if 'team' in keywords or 'collaborate' in keywords:
            strengths.append("Good teamwork and collaboration skills")
        if 'lead' in keywords or 'manage' in keywords:
            strengths.append("Leadership experience")
        if 'project' in keywords:
            strengths.append("Project management experience")
        
        # Remove duplicates and limit to 5 strengths
        unique_strengths = list(set(strengths))
        return unique_strengths[:5]

    def analyze_resume(self, resume_text):
        """
        Perform comprehensive analysis of a resume.
        
        Args:
            resume_text: The text content of the resume.
            
        Returns:
            Dictionary containing analysis results.
        """
        # Analyze each category
        category_scores = {}
        feedback = {}
        
        for category in self.job_descriptions.keys():
            score, category_feedback = self.analyze_category(resume_text, category)
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
        overall_score = round(overall_score)
        
        # Get improvement suggestions
        improvement_suggestions = self.get_improvement_suggestions(resume_text, category_scores)
        
        # Identify key strengths
        key_strengths = self.identify_key_strengths(resume_text, category_scores)
        
        # Identify likely job role
        job_role, confidence = self.identify_job_role(resume_text)
        
        # Extract keywords
        keywords = self.extract_keywords(resume_text, top_n=20)
        
        # Compile results
        results = {
            'score': overall_score,
            'category_scores': category_scores,
            'feedback': feedback,
            'improvement_suggestions': improvement_suggestions,
            'key_strengths': key_strengths,
            'job_role': job_role.replace('_', ' ').title(),
            'job_role_confidence': round(confidence * 100),
            'keywords': keywords
        }
        
        return results
