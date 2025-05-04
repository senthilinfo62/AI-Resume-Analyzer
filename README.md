# AI Resume Analyzer

A comprehensive AI-powered resume analysis platform that evaluates resumes and provides scores and feedback to users. The application follows clean architecture principles for maintainability and scalability.

## Project Overview

### Key Components

#### Architecture
- **Frontend**: React with TypeScript
- **Backend**: Django (Python)
- **Database**: MySQL
- **Containerization**: Docker
- **AI Model**: Advanced NLP-based resume analysis system

#### Core Features
- **User Authentication**: Account creation and login system
- **Resume Upload**: Secure file upload and storage
- **AI Analysis**: Sophisticated NLP-based resume evaluation with:
  - Overall scoring (0-100)
  - Category-specific scoring and detailed feedback
  - Job role identification with confidence score
  - Key strengths identification
  - Personalized improvement suggestions
  - Keyword extraction and analysis
- **Results Dashboard**: Visual representation of analysis results with interactive charts

### Clean Architecture Implementation
- **Domain Layer**: Core business entities and use cases
- **Adapters Layer**: Repositories and services
- **Interface Layer**: API endpoints and database models
- **Presentation Layer**: UI components and state management

### AI Component
The application features a sophisticated AI resume analyzer built with Python's natural language processing libraries:

#### Technologies Used
- **NLTK**: For text preprocessing, tokenization, and linguistic analysis
- **scikit-learn**: For TF-IDF vectorization and cosine similarity calculations
- **Pandas**: For data manipulation and analysis

#### Key AI Features
- **Advanced Text Analysis**: Preprocessing with tokenization, stopword removal, and lemmatization
- **Comprehensive Resume Evaluation**: Analysis of technical skills, education, experience, achievements, and formatting
- **Job Role Identification**: Matching resume content with different job profiles
- **Personalized Improvement Suggestions**: Tailored recommendations based on resume content and scores
- **Key Strengths Identification**: Highlighting positive aspects of the resume
- **Keyword Extraction**: Identifying important terms and their relevance

#### Technical Implementation
- **Text Preprocessing Pipeline**: Converts raw resume text into clean, normalized tokens
- **TF-IDF Vectorization**: Transforms text into numerical features for analysis
- **Cosine Similarity**: Measures similarity between resume content and reference texts
- **Category-Specific Analysis**: Specialized evaluation for different resume sections
- **Weighted Scoring System**: Calculates overall score based on category importance
- **Error Handling**: Graceful fallback mechanisms for robust operation

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.8+ (for local backend development)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. Start the application using Docker Compose:
   ```
   docker-compose up
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api
   - Admin interface: http://localhost:8000/admin

### Local Development

#### Frontend
```
cd frontend
npm install
npm run dev
```

#### Backend
```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Project Structure

```
ai-resume-analyzer/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   └── App.tsx           # Main application component
│   ├── package.json          # Frontend dependencies
│   └── Dockerfile            # Frontend Docker configuration
├── backend/                  # Django backend
│   ├── api/                  # Main application
│   │   ├── domain/           # Domain layer (entities, use cases)
│   │   ├── adapters/         # Adapters layer (repositories, services)
│   │   ├── interfaces/       # Interface layer (API endpoints)
│   │   ├── ai/               # AI module for resume analysis
│   │   │   └── resume_analyzer.py  # Advanced NLP-based resume analyzer
│   │   └── presentation/     # Presentation layer (if needed)
│   ├── resume_analyzer/      # Django project settings
│   ├── requirements.txt      # Backend dependencies
│   ├── download_nltk_data.py # Script to download NLTK data
│   └── Dockerfile            # Backend Docker configuration
└── docker-compose.yml        # Docker Compose configuration
```

## Troubleshooting

### Common Issues

#### MySQL Connection Issues
If you encounter issues with the MySQL connection, try the following:

1. Check if the MySQL container is running:
   ```
   docker-compose ps
   ```

2. Ensure the database credentials in the `.env` file match those in `docker-compose.yml`.

3. Rebuild the containers:
   ```
   docker-compose down
   docker-compose up --build
   ```

#### Frontend Not Loading
If the frontend is not loading properly, try the following:

1. Check if the frontend container is running:
   ```
   docker-compose ps
   ```

2. Check the frontend logs:
   ```
   docker-compose logs frontend
   ```

3. Ensure the `VITE_API_URL` environment variable is set correctly in `docker-compose.yml`.

#### Backend API Not Responding
If the backend API is not responding, try the following:

1. Check if the backend container is running:
   ```
   docker-compose ps
   ```

2. Check the backend logs:
   ```
   docker-compose logs backend
   ```

3. Ensure the database connection is properly configured.

## Default Credentials

After starting the application for the first time, you can log in to the admin interface with the following credentials:

- **Username**: admin
- **Password**: admin

## AI Analysis Process

The resume analysis process follows these steps:

1. **Resume Upload**: User uploads a resume file (PDF, DOCX, or TXT)
2. **Text Extraction**: System extracts text content from the uploaded file
3. **Preprocessing**: Text is cleaned, tokenized, and prepared for analysis
4. **Category Analysis**: Resume is analyzed across five key categories:
   - Technical Skills
   - Education
   - Experience
   - Achievements
   - Formatting
5. **Job Role Matching**: Resume content is matched against different job role profiles
6. **Keyword Extraction**: Important keywords are identified and ranked by relevance
7. **Score Calculation**: Overall and category-specific scores are calculated
8. **Feedback Generation**: Detailed feedback is generated for each category
9. **Suggestions Creation**: Personalized improvement suggestions are created
10. **Strengths Identification**: Key strengths of the resume are identified
11. **Results Presentation**: Analysis results are presented to the user in an interactive dashboard

### Analysis Categories

#### Technical Skills
Evaluates the presence and relevance of technical skills, programming languages, tools, and technologies mentioned in the resume.

#### Education
Analyzes educational background, degrees, institutions, academic achievements, and relevant coursework.

#### Experience
Evaluates professional experience, job roles, responsibilities, achievements, and career progression.

#### Achievements
Analyzes accomplishments, awards, recognitions, and measurable results mentioned in the resume.

#### Formatting
Evaluates the resume's layout, structure, readability, and overall presentation.

### Supported Job Roles

The AI analyzer can identify and provide tailored feedback for the following job roles:

- **Software Engineer**: Developers, programmers, full-stack, backend, and frontend engineers
- **Data Scientist**: Data analysts, machine learning engineers, and AI specialists
- **Product Manager**: Product owners and product development specialists
- **Marketing Professional**: Digital marketers, content marketers, and social media specialists
- **Finance Professional**: Financial analysts, accountants, and financial advisors

The system calculates a confidence score for each job role match, indicating how well the resume aligns with the specific role.

## Future AI Enhancements

The AI component is designed to be extensible and can be enhanced with the following features:

- **Advanced PDF Parsing**: Improved extraction of text from complex PDF layouts
- **Language Support**: Analysis of resumes in multiple languages
- **Industry-Specific Analysis**: Tailored analysis for different industries and sectors
- **Job Description Matching**: Comparing resumes against specific job descriptions
- **Trend Analysis**: Identifying trending skills and keywords in the job market
- **Competitive Analysis**: Comparing the resume against industry benchmarks
- **Interview Question Generation**: Creating potential interview questions based on resume content
- **Cover Letter Suggestions**: Generating cover letter content based on resume analysis
- **Career Path Recommendations**: Suggesting potential career paths based on skills and experience

## License

This project is licensed under the MIT License - see the LICENSE file for details.
