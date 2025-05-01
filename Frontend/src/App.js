import React from 'react';
import {
  Container,
  CssBaseline,
  ThemeProvider,
  createTheme,
  Typography
} from '@mui/material';
import { Routes, Route, Navigate } from 'react-router-dom';

import SongForm from './Components/SongForm';
import Header from './Components/Header';
import Footer from './Components/Footer';
import Dashboard from './Components/Dashboard';


// Create a custom theme with modern design elements
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#3a36e0', // Vibrant blue
      light: '#6d6ff8',
      dark: '#1c1aa8',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#ff6b6b', // Coral/salmon
      light: '#ff9a9a',
      dark: '#cf4848',
      contrastText: '#ffffff',
    },
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
    success: {
      main: '#00c853',
    },
    error: {
      main: '#ff3d71',
    },
    warning: {
      main: '#ffaa00',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      letterSpacing: '-0.01562em',
    },
    h2: {
      fontWeight: 700,
      fontSize: '2rem',
      letterSpacing: '-0.00833em',
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.75rem',
      letterSpacing: '0em',
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.5rem',
      letterSpacing: '0.00735em',
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem',
      letterSpacing: '0em',
    },
    h6: {
      fontWeight: 600,
      fontSize: '1rem',
      letterSpacing: '0.0075em',
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0px 2px 4px rgba(0,0,0,0.05)',
    '0px 4px 8px rgba(0,0,0,0.08)',
    '0px 8px 16px rgba(0,0,0,0.1)',
    // ... keep the rest of the default shadows
    ...Array(21).fill(''),
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          boxShadow: '0px 4px 12px rgba(0,0,0,0.08)',
          padding: '10px 24px',
          '&:hover': {
            boxShadow: '0px 6px 16px rgba(0,0,0,0.12)',
            transform: 'translateY(-2px)',
          },
          transition: 'all 0.2s ease-in-out',
        },
        containedPrimary: {
          background: 'linear-gradient(45deg, #3a36e0 30%, #5654f5 90%)',
        },
        containedSecondary: {
          background: 'linear-gradient(45deg, #ff6b6b 30%, #ff8e8e 90%)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: '0px 10px 40px -10px rgba(0,0,0,0.08)',
          transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
          '&:hover': {
            boxShadow: '0px 20px 40px -10px rgba(0,0,0,0.12)',
            transform: 'translateY(-4px)',
          },
        },
        elevation1: {
          boxShadow: '0px 2px 10px rgba(0,0,0,0.05)',
        },
        elevation2: {
          boxShadow: '0px 4px 20px rgba(0,0,0,0.08)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0px 2px 20px rgba(0,0,0,0.08)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            '&:hover fieldset': {
              borderColor: '#3a36e0',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#3a36e0',
              borderWidth: 2,
            },
          },
        },
      },
    },
    MuiSlider: {
      styleOverrides: {
        thumb: {
          boxShadow: '0px 2px 6px rgba(0,0,0,0.2)',
          '&:hover, &.Mui-active': {
            boxShadow: '0px 4px 8px rgba(0,0,0,0.3)',
          },
        },
        track: {
          borderRadius: 4,
          height: 8,
        },
        rail: {
          borderRadius: 4,
          height: 8,
        },
      },
    },
  },
});

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header />

      <Container
        maxWidth="lg"
        sx={{
          mt: 6,
          mb: 8,
          minHeight: 'calc(100vh - 180px)'
        }}
      >
        <Routes>

           {/* redirect root to /songs */}
           <Route path="/" element={<Navigate to="/songs" replace />} />

          {/* “My Songs” page */}
           <Route path="/songs" element={<SongForm />} />

          {/* Dashboard page */}
          <Route path="/dashboard" element={<Dashboard />} />

          {/* simple 404 fallback */}
          <Route
            path="*"
            element={
              <Typography variant="h6" align="center">
                404 – Page Not Found
              </Typography>
            }
          />
        </Routes>
      </Container>

      <Footer />
    </ThemeProvider>
  );
}