import { Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Divider,
  Button,
  Card,
  CardContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
} from '@mui/material';
import Grid from '../components/ui/Grid';
import {
  ExpandMore,
  ArrowBack,
} from '@mui/icons-material';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, RadialLinearScale } from 'chart.js';
import { Doughnut, PolarArea } from 'react-chartjs-2';
import { Resume } from '../services/resume';

// Register Chart.js components
ChartJS.register(ArcElement, RadialLinearScale, Tooltip, Legend);

// Static resume data for analysis
const staticResumeData: Resume & {
  improvementSuggestions?: string[];
  keyStrengths?: string[];
} = {
  id: 1,
  filename: "john_doe_resume.pdf",
  score: 78,
  uploadDate: "2023-05-04",
  feedback: {
    technical_skills: "Your technical skills section is strong, but consider organizing them by proficiency level. Add more details about your expertise in React and Node.js. Consider adding relevant certifications to strengthen this section.",
    education: "Education section is well-structured. Include GPA if it is above 3.5. Consider adding relevant coursework that aligns with your target positions. Highlight any academic achievements or leadership roles.",
    experience: "Your work experience is impressive, but use more action verbs and quantify your achievements with metrics. For example, Increased website performance by 40% instead of Improved website performance. Focus on outcomes rather than just responsibilities.",
    achievements: "Good list of achievements, but they could be more impactful. Quantify results where possible and connect them to business outcomes. Consider adding awards, recognitions, or publications if applicable.",
    formatting: "The resume layout is clean, but consider using a more modern template. Ensure consistent spacing and alignment throughout. Use bullet points for better readability and keep bullet points to 1-2 lines each."
  },
  categoryScores: {
    technical_skills: 82,
    education: 85,
    experience: 75,
    achievements: 70,
    formatting: 80
  },
  improvementSuggestions: [
    "Add metrics to quantify your achievements",
    "Include relevant certifications",
    "Organize skills by proficiency level",
    "Use more powerful action verbs",
    "Ensure consistent formatting throughout"
  ],
  keyStrengths: [
    "Comprehensive technical skill set",
    "Strong educational background",
    "Clear chronological work history",
    "Good overall organization",
    "Relevant industry experience"
  ]
};

const ResumeAnalysis = () => {
  // Using static data instead of fetching from API
  const resumeData = staticResumeData;

  // Prepare chart data
  const doughnutData = {
    labels: ['Score', 'Remaining'],
    datasets: [
      {
        data: [resumeData.score || 0, 100 - (resumeData.score || 0)],
        backgroundColor: [
          (resumeData.score || 0) >= 80 ? '#4caf50' : (resumeData.score || 0) >= 60 ? '#ff9800' : '#f44336',
          '#e0e0e0',
        ],
        borderWidth: 0,
      },
    ],
  };

  // Default category scores if not available
  const defaultCategoryScores = {
    technical_skills: 0,
    education: 0,
    experience: 0,
    achievements: 0,
    formatting: 0,
  };

  const categoryScores = resumeData.categoryScores || defaultCategoryScores;

  const categoryData = {
    labels: [
      'Technical Skills',
      'Education',
      'Experience',
      'Achievements',
      'Formatting',
    ],
    datasets: [
      {
        data: [
          categoryScores.technical_skills,
          categoryScores.education,
          categoryScores.experience,
          categoryScores.achievements,
          categoryScores.formatting,
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(153, 102, 255, 0.7)',
          'rgba(255, 159, 64, 0.7)',
          'rgba(255, 99, 132, 0.7)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <Container maxWidth={false} sx={{ mt: 4, mb: 4, px: { xs: 2, sm: 3, md: 4 } }}>
      <Button
        component={RouterLink}
        to="/"
        startIcon={<ArrowBack />}
        sx={{ mb: 3 }}
      >
        Back to Dashboard
      </Button>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom>
              Overall Score
            </Typography>
            <Box sx={{ height: 200, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              <Box sx={{ position: 'relative', width: 180, height: 180 }}>
                <Doughnut data={doughnutData} options={{ cutout: '80%' }} />
                <Box
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'column',
                  }}
                >
                  <Typography variant="h3" component="div" sx={{ fontWeight: 'bold' }}>
                    {resumeData.score}
                  </Typography>
                  <Typography variant="body2" component="div">
                    out of 100
                  </Typography>
                </Box>
              </Box>
            </Box>
            <Typography
              variant="h6"
              sx={{
                mt: 2,
                color:
                  (resumeData.score || 0) >= 80
                    ? 'success.main'
                    : (resumeData.score || 0) >= 60
                    ? 'warning.main'
                    : 'error.main',
              }}
            >
              {(resumeData.score || 0) >= 80
                ? 'Excellent'
                : (resumeData.score || 0) >= 60
                ? 'Good'
                : 'Needs Improvement'}
            </Typography>
          </Paper>

          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resume Details
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body2" gutterBottom>
                <strong>Filename:</strong> {resumeData.filename}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Uploaded:</strong> {resumeData.uploadDate}
              </Typography>
              <Button
                variant="outlined"
                fullWidth
                sx={{ mt: 2 }}
                // In a real app, this would download the resume
              >
                Download Resume
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Category Breakdown
            </Typography>
            <Box sx={{ height: 300, mb: 4 }}>
              <PolarArea data={categoryData} />
            </Box>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              Key Strengths
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box sx={{ mb: 4 }}>
              {resumeData.keyStrengths?.map((strength, index) => (
                <Chip
                  key={index}
                  label={strength}
                  color="success"
                  variant="outlined"
                  sx={{ m: 0.5, fontSize: '0.9rem', py: 0.5 }}
                />
              ))}
            </Box>

            <Typography variant="h5" gutterBottom>
              Areas for Improvement
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box sx={{ mb: 4 }}>
              {resumeData.improvementSuggestions?.map((suggestion, index) => (
                <Chip
                  key={index}
                  label={suggestion}
                  color="warning"
                  variant="outlined"
                  sx={{ m: 0.5, fontSize: '0.9rem', py: 0.5 }}
                />
              ))}
            </Box>

            <Typography variant="h5" gutterBottom>
              Detailed Feedback
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6">Technical Skills</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body1">{resumeData.feedback?.technical_skills || 'No feedback available'}</Typography>
              </AccordionDetails>
            </Accordion>

            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6">Education</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body1">{resumeData.feedback?.education || 'No feedback available'}</Typography>
              </AccordionDetails>
            </Accordion>

            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6">Experience</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body1">{resumeData.feedback?.experience || 'No feedback available'}</Typography>
              </AccordionDetails>
            </Accordion>

            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6">Achievements</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body1">{resumeData.feedback?.achievements || 'No feedback available'}</Typography>
              </AccordionDetails>
            </Accordion>

            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6">Formatting</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body1">{resumeData.feedback?.formatting || 'No feedback available'}</Typography>
              </AccordionDetails>
            </Accordion>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ResumeAnalysis;
