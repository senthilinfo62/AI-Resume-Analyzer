import { Container, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const NotFound = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 8, textAlign: 'center' }}>
      <Typography variant="h1" component="h1" gutterBottom>
        404
      </Typography>
      <Typography variant="h4" component="h2" gutterBottom>
        Page Not Found
      </Typography>
      <Typography variant="body1" paragraph>
        The page you are looking for does not exist or has been moved.
      </Typography>
      <Box sx={{ mt: 4 }}>
        <Button variant="contained" component={RouterLink} to="/">
          Go to Home
        </Button>
      </Box>
    </Container>
  );
};

export default NotFound;
