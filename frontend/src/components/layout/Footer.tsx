import { Box, Typography, Container, Stack, Link, Divider } from '@mui/material';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import GitHubIcon from '@mui/icons-material/GitHub';
import TwitterIcon from '@mui/icons-material/Twitter';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 4,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[900],
        color: 'white',
        width: '100%'
      }}
    >
      <Container maxWidth={false} sx={{ width: '100%', px: { xs: 2, sm: 3, md: 4 } }}>
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          spacing={4}
          justifyContent="space-between"
          divider={<Divider orientation="vertical" flexItem sx={{ display: { xs: 'none', sm: 'block' }, backgroundColor: 'grey.700' }} />}
        >
          <Box>
            <Typography variant="h6" gutterBottom>
              AI Resume Analyzer
            </Typography>
            <Typography variant="body2" color="grey.400">
              An intelligent tool to analyze and improve your resume for better job opportunities.
            </Typography>
          </Box>

          <Box>
            <Typography variant="h6" gutterBottom>
              Quick Links
            </Typography>
            <Link href="/" color="inherit" sx={{ display: 'block', mb: 1 }}>
              Home
            </Link>
            <Link href="/upload" color="inherit" sx={{ display: 'block', mb: 1 }}>
              Upload Resume
            </Link>
            <Link href="/login" color="inherit" sx={{ display: 'block', mb: 1 }}>
              Login
            </Link>
            <Link href="/register" color="inherit" sx={{ display: 'block' }}>
              Register
            </Link>
          </Box>

          <Box>
            <Typography variant="h6" gutterBottom>
              Connect With Us
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Link href="#" color="inherit">
                <LinkedInIcon />
              </Link>
              <Link href="#" color="inherit">
                <GitHubIcon />
              </Link>
              <Link href="#" color="inherit">
                <TwitterIcon />
              </Link>
            </Box>
          </Box>
        </Stack>

        <Divider sx={{ my: 3, backgroundColor: 'grey.700' }} />
        <Typography variant="body2" color="grey.400" align="center">
          © {new Date().getFullYear()} AI Resume Analyzer. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
