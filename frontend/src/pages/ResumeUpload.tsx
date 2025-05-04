import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import { CloudUpload, CheckCircle, Description } from '@mui/icons-material';
import ResumeService from '../services/resume';

const ResumeUpload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const selectedFile = event.target.files[0];

      // Validate file type
      const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      if (!allowedTypes.includes(selectedFile.type)) {
        setError('Please upload a PDF, Word document, or text file.');
        setFile(null);
        return;
      }

      // Validate file size (max 5MB)
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError('File size cannot exceed 5MB.');
        setFile(null);
        return;
      }

      setFile(selectedFile);
      setError(null);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Upload the resume
      const resume = await ResumeService.uploadResume(file);

      setSuccess(true);

      // Redirect to the analysis page after a short delay
      setTimeout(() => {
        navigate(`/analysis/${resume.id}`);
      }, 1500);
    } catch (err) {
      console.error('Upload error:', err);
      setError('Failed to upload resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth={false} sx={{ mt: 4, mb: 4, px: { xs: 2, sm: 3, md: 4 } }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Upload Your Resume
        </Typography>

        <Typography variant="body1" sx={{ mb: 2 }} align="center">
          Upload your resume to get an AI-powered analysis and score.
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            Resume uploaded successfully! Redirecting to analysis...
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Box
            sx={{
              border: '2px dashed #ccc',
              borderRadius: 2,
              p: 3,
              textAlign: 'center',
              mb: 3,
              backgroundColor: '#f9f9f9',
            }}
          >
            <input
              accept=".pdf,.doc,.docx,.txt"
              style={{ display: 'none' }}
              id="resume-file"
              type="file"
              onChange={handleFileChange}
              disabled={loading || success}
            />
            <label htmlFor="resume-file">
              <Button
                variant="contained"
                component="span"
                startIcon={<CloudUpload />}
                disabled={loading || success}
              >
                Select File
              </Button>
            </label>

            {file && (
              <Box sx={{ mt: 2 }}>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <Description />
                    </ListItemIcon>
                    <ListItemText
                      primary={file.name}
                      secondary={`${(file.size / 1024).toFixed(2)} KB`}
                    />
                  </ListItem>
                </List>
              </Box>
            )}
          </Box>

          <Box sx={{ textAlign: 'center' }}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              size="large"
              disabled={!file || loading || success}
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : success ? <CheckCircle /> : null}
            >
              {loading ? 'Uploading...' : success ? 'Uploaded' : 'Upload Resume'}
            </Button>
          </Box>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Supported File Formats
          </Typography>
          <Typography variant="body2">
            • PDF (.pdf)<br />
            • Microsoft Word (.doc, .docx)<br />
            • Text (.txt)
          </Typography>

          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Tips for Better Results
          </Typography>
          <Typography variant="body2">
            • Make sure your resume is up-to-date<br />
            • Include relevant skills and experience<br />
            • Use a clean, professional format<br />
            • Proofread for spelling and grammar errors
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default ResumeUpload;
