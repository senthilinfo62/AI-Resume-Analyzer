import {
  Box,
  Typography,
  Paper,
  Divider,
  Chip,
  LinearProgress,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  ExpandMore,
  CheckCircle,
  Cancel,
  TrendingUp,
  Code,
  Psychology,
  Business,
} from '@mui/icons-material';

interface JobMatchProps {
  jobMatch: {
    overall_match_score: number;
    similarity_score: number;
    skill_match_scores: Record<string, number>;
    missing_skills: Record<string, string[]>;
    matched_skills: Record<string, string[]>;
    job_specific_suggestions: string[];
  };
}

const JobMatchResults = ({ jobMatch }: JobMatchProps) => {
  // Helper function to get color based on score
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'success.main';
    if (score >= 60) return 'warning.main';
    return 'error.main';
  };

  // Helper function to get text based on score
  const getScoreText = (score: number) => {
    if (score >= 80) return 'Excellent Match';
    if (score >= 60) return 'Good Match';
    return 'Needs Improvement';
  };

  // Helper function to get icon for skill category
  const getSkillIcon = (category: string) => {
    switch (category) {
      case 'technical':
        return <Code />;
      case 'soft':
        return <Psychology />;
      case 'domain':
        return <Business />;
      default:
        return <TrendingUp />;
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Job Match Results
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {/* Overall Match Score */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Overall Match Score
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Box sx={{ width: '100%', mr: 1 }}>
            <LinearProgress
              variant="determinate"
              value={jobMatch.overall_match_score}
              sx={{
                height: 10,
                borderRadius: 5,
                backgroundColor: 'grey.300',
                '& .MuiLinearProgress-bar': {
                  borderRadius: 5,
                  backgroundColor: getScoreColor(jobMatch.overall_match_score),
                },
              }}
            />
          </Box>
          <Box sx={{ minWidth: 35 }}>
            <Typography variant="body2" color="text.secondary">{`${Math.round(
              jobMatch.overall_match_score
            )}%`}</Typography>
          </Box>
        </Box>
        <Typography
          variant="subtitle1"
          sx={{ color: getScoreColor(jobMatch.overall_match_score) }}
        >
          {getScoreText(jobMatch.overall_match_score)}
        </Typography>
      </Box>

      {/* Skill Category Scores */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Skill Category Scores
        </Typography>
        <Grid container spacing={2}>
          {Object.entries(jobMatch.skill_match_scores).map(([category, score]) => (
            <Grid item xs={12} sm={4} key={category}>
              <Box sx={{ textAlign: 'center', p: 2, border: 1, borderColor: 'divider', borderRadius: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
                  {getSkillIcon(category)}
                </Box>
                <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
                  {category} Skills
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <Box sx={{ width: '100%', mr: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={score}
                      sx={{
                        height: 8,
                        borderRadius: 5,
                        backgroundColor: 'grey.300',
                        '& .MuiLinearProgress-bar': {
                          borderRadius: 5,
                          backgroundColor: getScoreColor(score),
                        },
                      }}
                    />
                  </Box>
                  <Box sx={{ minWidth: 35 }}>
                    <Typography variant="body2" color="text.secondary">{`${Math.round(score)}%`}</Typography>
                  </Box>
                </Box>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Matched vs Missing Skills */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Skills Analysis
        </Typography>

        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="subtitle1">Technical Skills</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="success.main" sx={{ display: 'flex', alignItems: 'center' }}>
                  <CheckCircle fontSize="small" sx={{ mr: 1 }} />
                  Matched Skills
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {jobMatch.matched_skills.technical.length > 0 ? (
                    jobMatch.matched_skills.technical.map((skill) => (
                      <Chip
                        key={skill}
                        label={skill}
                        color="success"
                        variant="outlined"
                        size="small"
                        sx={{ m: 0.5 }}
                      />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No matched technical skills found
                    </Typography>
                  )}
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="error.main" sx={{ display: 'flex', alignItems: 'center' }}>
                  <Cancel fontSize="small" sx={{ mr: 1 }} />
                  Missing Skills
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {jobMatch.missing_skills.technical.length > 0 ? (
                    jobMatch.missing_skills.technical.map((skill) => (
                      <Chip
                        key={skill}
                        label={skill}
                        color="error"
                        variant="outlined"
                        size="small"
                        sx={{ m: 0.5 }}
                      />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No missing technical skills found
                    </Typography>
                  )}
                </Box>
              </Grid>
            </Grid>
          </AccordionDetails>
        </Accordion>

        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="subtitle1">Soft Skills</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="success.main" sx={{ display: 'flex', alignItems: 'center' }}>
                  <CheckCircle fontSize="small" sx={{ mr: 1 }} />
                  Matched Skills
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {jobMatch.matched_skills.soft.length > 0 ? (
                    jobMatch.matched_skills.soft.map((skill) => (
                      <Chip
                        key={skill}
                        label={skill}
                        color="success"
                        variant="outlined"
                        size="small"
                        sx={{ m: 0.5 }}
                      />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No matched soft skills found
                    </Typography>
                  )}
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="error.main" sx={{ display: 'flex', alignItems: 'center' }}>
                  <Cancel fontSize="small" sx={{ mr: 1 }} />
                  Missing Skills
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {jobMatch.missing_skills.soft.length > 0 ? (
                    jobMatch.missing_skills.soft.map((skill) => (
                      <Chip
                        key={skill}
                        label={skill}
                        color="error"
                        variant="outlined"
                        size="small"
                        sx={{ m: 0.5 }}
                      />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No missing soft skills found
                    </Typography>
                  )}
                </Box>
              </Grid>
            </Grid>
          </AccordionDetails>
        </Accordion>

        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="subtitle1">Domain Knowledge</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="success.main" sx={{ display: 'flex', alignItems: 'center' }}>
                  <CheckCircle fontSize="small" sx={{ mr: 1 }} />
                  Matched Knowledge
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {jobMatch.matched_skills.domain.length > 0 ? (
                    jobMatch.matched_skills.domain.map((skill) => (
                      <Chip
                        key={skill}
                        label={skill}
                        color="success"
                        variant="outlined"
                        size="small"
                        sx={{ m: 0.5 }}
                      />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No matched domain knowledge found
                    </Typography>
                  )}
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="error.main" sx={{ display: 'flex', alignItems: 'center' }}>
                  <Cancel fontSize="small" sx={{ mr: 1 }} />
                  Missing Knowledge
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {jobMatch.missing_skills.domain.length > 0 ? (
                    jobMatch.missing_skills.domain.map((skill) => (
                      <Chip
                        key={skill}
                        label={skill}
                        color="error"
                        variant="outlined"
                        size="small"
                        sx={{ m: 0.5 }}
                      />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No missing domain knowledge found
                    </Typography>
                  )}
                </Box>
              </Grid>
            </Grid>
          </AccordionDetails>
        </Accordion>
      </Box>

      {/* Job-Specific Suggestions */}
      <Box sx={{ mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          Job-Specific Improvement Suggestions
        </Typography>
        <List>
          {jobMatch.job_specific_suggestions.map((suggestion, index) => (
            <ListItem key={index}>
              <ListItemIcon>
                <TrendingUp color="primary" />
              </ListItemIcon>
              <ListItemText primary={suggestion} />
            </ListItem>
          ))}
        </List>
      </Box>
    </Paper>
  );
};

export default JobMatchResults;
