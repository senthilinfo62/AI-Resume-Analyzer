import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  CircularProgress,
  Chip,
  Divider,
  Paper,
  CardHeader,
  CardActions,
  Avatar
} from '@mui/material';
import Grid from '../components/ui/Grid';
import { Link as RouterLink } from 'react-router-dom';
import ResumeService, { Resume } from '../services/resume';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DescriptionIcon from '@mui/icons-material/Description';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';

const Dashboard = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await ResumeService.getResumes();
        setResumes(data);
      } catch (err) {
        console.error('Error fetching resumes:', err);
        setError('Failed to load resumes. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, []);

  return (
    <Container maxWidth={false} sx={{ mt: 4, mb: 4, px: { xs: 2, sm: 3, md: 4 } }}>
      <Paper
        elevation={0}
        sx={{
          p: 3,
          mb: 4,
          borderRadius: 2,
          background: 'linear-gradient(135deg, #3f51b5 0%, #5c6bc0 100%)',
          color: 'white'
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h4" component="h1" fontWeight="500" gutterBottom>
              Your Resume Dashboard
            </Typography>
            <Typography variant="subtitle1">
              Manage and analyze your resumes to improve your job prospects
            </Typography>
          </Box>
          <Button
            variant="contained"
            color="secondary"
            component={RouterLink}
            to="/upload"
            startIcon={<UploadFileIcon />}
            sx={{
              py: 1.2,
              px: 3,
              fontWeight: 600,
              boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
              '&:hover': {
                boxShadow: '0 6px 10px rgba(0,0,0,0.2)',
              }
            }}
          >
            Upload New Resume
          </Button>
        </Box>
      </Paper>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
          <CircularProgress size={60} />
        </Box>
      ) : error ? (
        <Paper
          elevation={0}
          sx={{
            p: 3,
            borderRadius: 2,
            bgcolor: '#ffebee',
            border: '1px solid #ffcdd2'
          }}
        >
          <Typography variant="body1" color="error" sx={{ display: 'flex', alignItems: 'center' }}>
            {error}
          </Typography>
        </Paper>
      ) : resumes.length === 0 ? (
        <Paper
          elevation={3}
          sx={{
            p: 5,
            borderRadius: 2,
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2
          }}
        >
          <DescriptionIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            No Resumes Found
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3, maxWidth: '600px' }}>
            You haven't uploaded any resumes yet. Upload your resume to get AI-powered analysis and improvement suggestions.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            component={RouterLink}
            to="/upload"
            startIcon={<UploadFileIcon />}
            size="large"
          >
            Upload Your First Resume
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {resumes.map((resume) => (
            <Grid item xs={12} md={4} key={resume.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  borderRadius: 2,
                  overflow: 'hidden'
                }}
              >
                <CardHeader
                  avatar={
                    <Avatar sx={{ bgcolor: 'primary.main' }}>
                      <DescriptionIcon />
                    </Avatar>
                  }
                  title={
                    <Typography variant="h6" component="div" noWrap>
                      {resume.filename}
                    </Typography>
                  }
                  subheader={
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                      <CalendarTodayIcon sx={{ fontSize: 16, mr: 0.5, color: 'text.secondary' }} />
                      <Typography variant="body2" color="text.secondary">
                        {resume.uploadDate}
                      </Typography>
                    </Box>
                  }
                />
                <Divider />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Resume Score
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {resume.score ? (
                        <Chip
                          label={`${resume.score}/100`}
                          color={resume.score >= 80 ? 'success' : resume.score >= 60 ? 'warning' : 'error'}
                          sx={{
                            fontWeight: 'bold',
                            fontSize: '1rem',
                            height: 32
                          }}
                        />
                      ) : (
                        <Chip
                          label="Pending Analysis"
                          color="default"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </Box>

                  {resume.score && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        Rating
                      </Typography>
                      <Typography variant="body1">
                        {resume.score >= 80 ? 'Excellent' :
                         resume.score >= 70 ? 'Very Good' :
                         resume.score >= 60 ? 'Good' :
                         resume.score >= 50 ? 'Average' : 'Needs Improvement'}
                      </Typography>
                    </Box>
                  )}
                </CardContent>
                <CardActions sx={{ p: 2, pt: 0 }}>
                  <Button
                    variant="contained"
                    color={resume.score ? "primary" : "secondary"}
                    component={RouterLink}
                    to={`/analysis/${resume.id}`}
                    fullWidth
                    startIcon={<AnalyticsIcon />}
                    sx={{
                      py: 1,
                      fontWeight: 500
                    }}
                  >
                    {resume.score ? 'View Analysis' : 'Analyze Resume'}
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default Dashboard;
