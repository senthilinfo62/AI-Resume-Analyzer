# AI Resume Analyzer

A comprehensive AI-powered resume analysis platform that evaluates resumes and provides scores and feedback to users. The application follows clean architecture principles for maintainability and scalability.

## Project Overview

### Key Components

#### Architecture
- **Frontend**: React with TypeScript
- **Backend**: Django (Python)
- **Database**: MySQL
- **Containerization**: Docker
- **AI Model**: Resume scoring and feedback system

#### Core Features
- **User Authentication**: Account creation and login system
- **Resume Upload**: Secure file upload and storage
- **AI Analysis**: Automated scoring (0-100) and detailed feedback
- **Results Dashboard**: Visual representation of analysis results

### Clean Architecture Implementation
- **Domain Layer**: Core business entities and use cases
- **Adapters Layer**: Repositories and services
- **Interface Layer**: API endpoints and database models
- **Presentation Layer**: UI components and state management

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
│   │   └── presentation/     # Presentation layer (if needed)
│   ├── resume_analyzer/      # Django project settings
│   ├── requirements.txt      # Backend dependencies
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.
