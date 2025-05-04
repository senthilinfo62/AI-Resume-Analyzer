import { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  CircularProgress,
  Alert,
} from '@mui/material';
import { WorkOutline, CompareArrows } from '@mui/icons-material';

interface JobComparisonFormProps {
  resumeId: number;
  onSubmit: (jobData: {
    title: string;
    description: string;
    company?: string;
    location?: string;
  }) => Promise<void>;
  isLoading?: boolean;
}

const JobComparisonForm = ({ resumeId, onSubmit, isLoading = false }: JobComparisonFormProps) => {
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [company, setCompany] = useState('');
  const [location, setLocation] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!jobTitle.trim()) {
      setError('Job title is required');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Job description is required');
      return;
    }

    try {
      await onSubmit({
        title: jobTitle,
        description: jobDescription,
        company,
        location,
      });
    } catch (err) {
      setError('Failed to compare resume with job description');
      console.error(err);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <CompareArrows sx={{ mr: 1 }} />
        Compare with Job Description
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Enter a job description to see how well your resume matches the requirements.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit} noValidate>
        <TextField
          margin="normal"
          required
          fullWidth
          id="jobTitle"
          label="Job Title"
          name="jobTitle"
          autoComplete="off"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          disabled={isLoading}
          InputProps={{
            startAdornment: <WorkOutline sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
        />

        <TextField
          margin="normal"
          fullWidth
          id="company"
          label="Company (Optional)"
          name="company"
          autoComplete="off"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          disabled={isLoading}
        />

        <TextField
          margin="normal"
          fullWidth
          id="location"
          label="Location (Optional)"
          name="location"
          autoComplete="off"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          disabled={isLoading}
        />

        <TextField
          margin="normal"
          required
          fullWidth
          id="jobDescription"
          label="Job Description"
          name="jobDescription"
          autoComplete="off"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          disabled={isLoading}
          multiline
          rows={6}
          placeholder="Paste the full job description here..."
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          disabled={isLoading}
          startIcon={isLoading ? <CircularProgress size={20} /> : <CompareArrows />}
        >
          {isLoading ? 'Comparing...' : 'Compare Resume with Job'}
        </Button>
      </Box>
    </Paper>
  );
};

export default JobComparisonForm;
