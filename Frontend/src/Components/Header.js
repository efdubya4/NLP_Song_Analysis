// src/Components/Header.js
import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  useMediaQuery,
  useTheme,
  Container,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LibraryMusicIcon from '@mui/icons-material/LibraryMusic';
import HistoryIcon from '@mui/icons-material/History';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

export default function Header() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [drawerOpen, setDrawerOpen] = useState(false);

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

  const navigationItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, to: '/dashboard' },
    { text: 'My Songs', icon: <LibraryMusicIcon />, to: '/songs' },
    { text: 'Analysis History', icon: <HistoryIcon />, to: '/history' },
    { text: 'Help', icon: <HelpOutlineIcon />, to: '/help' }
  ];

  const drawer = (
    <Box
      sx={{ width: 250 }}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          p: 2,
          background: 'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)',
          color: 'white'
        }}
      >
        <MusicNoteIcon sx={{ mr: 1 }} />
        <Typography variant="h6">SongPredictor</Typography>
      </Box>
      <Divider />
      <List>
        {navigationItems.map(({ text, icon, to }) => (
          <ListItem
            button
            key={text}
            component={RouterLink}
            to={to}
            sx={{ py: 1.5 }}
          >
            <ListItemIcon sx={{ color: 'primary.main', minWidth: 40 }}>
              {icon}
            </ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar
        position="sticky"
        elevation={0}
        sx={{
          backgroundColor: 'background.paper',
          borderBottom: '1px solid',
          borderColor: 'divider',
          color: 'text.primary'
        }}
      >
        <Container maxWidth="lg">
          <Toolbar disableGutters sx={{ height: 70 }}>
            {isMobile && (
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={toggleDrawer(true)}
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
            )}

            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                background: 'linear-gradient(135deg, #e0c3fc, #8ec5fc)',
                p: '8px 16px',
                borderRadius: 2,
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                mr: 2
              }}
            >
              <MusicNoteIcon sx={{ color: 'white' }} />
              <Typography
                variant="h6"
                component="div"
                sx={{ fontWeight: 700, color: 'white', letterSpacing: '0.5px' }}
              >
                SP
              </Typography>
            </Box>

            <Typography
              variant="h5"
              component="div"
              sx={{
                fontWeight: 700,
                fontSize: { xs: '1.2rem', md: '1.5rem' },
                background: 'linear-gradient(45deg, #ff9a9e, #fad0c4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                flexGrow: isMobile ? 1 : 0
              }}
            >
              SongPredictor
            </Typography>

            {!isMobile && (
              <Box sx={{ flexGrow: 1, display: 'flex', gap: 1.5, alignItems: 'center' }}>
                {navigationItems.map(({ text, icon, to }) => (
                  <Button
                    key={text}
                    component={RouterLink}
                    to={to}
                    color="inherit"
                    startIcon={icon}
                    sx={{
                      fontWeight: 500,
                      mx: 0.5,
                      py: 1,
                      borderRadius: 2,
                      '&:hover': { backgroundColor: 'rgba(0,0,0,0.05)' }
                    }}
                  >
                    {text}
                  </Button>
                ))}

                <Button
                  variant="contained"
                  color="primary"
                  disableElevation
                  sx={{
                    ml: 2,
                    fontWeight: 600,
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #f6d365, #fda085)',
                    boxShadow: '0 4px 14px rgba(253, 160, 133, 0.3) !important'
                  }}
                >
                  New Prediction
                </Button>
              </Box>
            )}

            {isMobile && (
              <Button
                variant="contained"
                color="primary"
                size="small"
                disableElevation
                sx={{
                  ml: 'auto',
                  fontWeight: 600,
                  borderRadius: 2,
                  background: 'linear-gradient(135deg, #f6d365, #fda085)',
                  boxShadow: '0 4px 14px rgba(253, 160, 133, 0.3) !important'
                }}
              >
                New
              </Button>
            )}
          </Toolbar>
        </Container>
      </AppBar>

      <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
        {drawer}
      </Drawer>
    </>
  );
}

