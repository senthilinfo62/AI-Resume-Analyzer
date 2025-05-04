import { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
  IconButton,
  Menu,
  MenuItem
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import DescriptionIcon from '@mui/icons-material/Description';
import { Link as RouterLink } from 'react-router-dom';

interface HeaderProps {
  isAuthenticated: boolean;
  onLogout: () => void;
}

const Header = ({ isAuthenticated, onLogout }: HeaderProps) => {
  const [mobileMenuAnchorEl, setMobileMenuAnchorEl] = useState<null | HTMLElement>(null);

  const handleMobileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setMobileMenuAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setMobileMenuAnchorEl(null);
  };

  const handleLogout = () => {
    handleMenuClose();
    onLogout();
  };

  return (
    <AppBar position="static" elevation={0} sx={{
      backgroundColor: 'primary.main',
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    }}>
      <Container maxWidth={false}>
        <Toolbar disableGutters>
          <DescriptionIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontWeight: 700,
              letterSpacing: '.1rem',
              color: 'white',
              textDecoration: 'none',
              flexGrow: 1
            }}
          >
            AI RESUME ANALYZER
          </Typography>

          {/* Mobile menu icon */}
          <Box sx={{ display: { xs: 'flex', md: 'none' }, flexGrow: 1 }}>
            <IconButton
              size="large"
              aria-label="menu"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMobileMenuOpen}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={mobileMenuAnchorEl}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(mobileMenuAnchorEl)}
              onClose={handleMenuClose}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {isAuthenticated ? (
                [
                  <MenuItem key="dashboard" component={RouterLink} to="/" onClick={handleMenuClose}>
                    Dashboard
                  </MenuItem>,
                  <MenuItem key="upload" component={RouterLink} to="/upload" onClick={handleMenuClose}>
                    Upload Resume
                  </MenuItem>,
                  <MenuItem key="logout" onClick={handleLogout}>
                    Logout
                  </MenuItem>
                ]
              ) : (
                [
                  <MenuItem key="login" component={RouterLink} to="/login" onClick={handleMenuClose}>
                    Login
                  </MenuItem>,
                  <MenuItem key="register" component={RouterLink} to="/register" onClick={handleMenuClose}>
                    Register
                  </MenuItem>
                ]
              )}
            </Menu>
          </Box>

          {/* Mobile title */}
          <DescriptionIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/"
            sx={{
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontWeight: 700,
              letterSpacing: '.1rem',
              color: 'white',
              textDecoration: 'none',
            }}
          >
            AI RESUME
          </Typography>

          {/* Desktop menu */}
          <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
            {isAuthenticated ? (
              <>
                <Button
                  color="inherit"
                  component={RouterLink}
                  to="/"
                  sx={{ mx: 1, '&:hover': { backgroundColor: 'primary.dark' } }}
                >
                  Dashboard
                </Button>
                <Button
                  color="inherit"
                  component={RouterLink}
                  to="/upload"
                  sx={{ mx: 1, '&:hover': { backgroundColor: 'primary.dark' } }}
                >
                  Upload Resume
                </Button>
                <Button
                  color="inherit"
                  onClick={onLogout}
                  sx={{ mx: 1, '&:hover': { backgroundColor: 'primary.dark' } }}
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button
                  color="inherit"
                  component={RouterLink}
                  to="/login"
                  sx={{ mx: 1, '&:hover': { backgroundColor: 'primary.dark' } }}
                >
                  Login
                </Button>
                <Button
                  variant="outlined"
                  color="inherit"
                  component={RouterLink}
                  to="/register"
                  sx={{
                    mx: 1,
                    borderColor: 'white',
                    '&:hover': {
                      backgroundColor: 'white',
                      color: 'primary.main'
                    }
                  }}
                >
                  Register
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;
