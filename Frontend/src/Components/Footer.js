import React from 'react';
import { Box, Container, Typography, Link, Grid, Divider, IconButton, useTheme } from '@mui/material';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

export default function Footer() {
  const theme = useTheme();
  const year = new Date().getFullYear();

  return (
    <Box 
      component="footer" 
      sx={{
        py: 4,
        background: 'linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%)',
        borderTop: '1px solid',
        borderColor: 'divider',
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center',
              mb: 2
            }}>
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center',
                background: 'linear-gradient(45deg, #ffdde1, #ee9ca7)',
                p: '6px 12px',
                borderRadius: 2,
                boxShadow: '0 4px 10px rgba(238, 156, 167, 0.2)',
                mr: 1.5
              }}>
                <MusicNoteIcon sx={{ color: 'white', fontSize: 18 }} />
                <Typography 
                  variant="body1" 
                  component="div" 
                  sx={{ 
                    fontWeight: 700, 
                    color: 'white',
                    fontSize: 14
                  }}
                >
                  SP
                </Typography>
              </Box>

              <Typography 
                variant="h6" 
                sx={{ 
                  fontWeight: 700,
                  background: 'linear-gradient(90deg, #ff9a9e, #fad0c4)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                SongPredictor
              </Typography>
            </Box>

            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Predict your song's hit potential with our advanced AI analysis.
              Get insights on what makes a hit and how to improve your music.
            </Typography>

            <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
              {[FacebookIcon, TwitterIcon, InstagramIcon, LinkedInIcon].map((Icon, i) => (
                <IconButton 
                  key={i}
                  aria-label={Icon.displayName || Icon.name} 
                  size="small"
                  sx={{ 
                    color: 'text.secondary',
                    '&:hover': {
                      color: '#ee9ca7',
                      backgroundColor: 'rgba(238, 156, 167, 0.1)'
                    }
                  }}
                >
                  <Icon fontSize="small" />
                </IconButton>
              ))}
            </Box>
          </Grid>

          {[['Product', ['Features', 'Pricing', 'Case Studies', 'Reviews', 'Updates']],
            ['Resources', ['Blog', 'Guides', 'Help Center', 'Webinars', 'API Docs']],
            ['Company', ['About', 'Team', 'Careers', 'Contact Us', 'Partners']],
            ['Legal', ['Terms', 'Privacy', 'Cookies', 'Licenses', 'Settings']]
          ].map(([section, links]) => (
            <Grid item xs={6} sm={4} md={2} key={section}>
              <Typography variant="subtitle2" color="text.primary" fontWeight={600} gutterBottom>
                {section}
              </Typography>
              <Box component="ul" sx={{ listStyle: 'none', p: 0, m: 0 }}>
                {links.map((item) => (
                  <Box component="li" key={item} sx={{ py: 0.5 }}>
                    <Link 
                      href="#" 
                      color="text.secondary" 
                      underline="hover"
                      sx={{ 
                        fontSize: '0.875rem',
                        '&:hover': {
                          color: 'primary.main',
                        }
                      }}
                    >
                      {item}
                    </Link>
                  </Box>
                ))}
              </Box>
            </Grid>
          ))}
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Box 
          sx={{
            display: 'flex',
            flexDirection: { xs: 'column', sm: 'row' },
            alignItems: { xs: 'flex-start', sm: 'center' },
            justifyContent: 'space-between',
          }}
        >
          <Typography variant="body2" color="text.secondary">
            © {year} SongPredictor. All rights reserved.
          </Typography>

          <Box 
            sx={{ 
              display: 'flex', 
              gap: 3,
              mt: { xs: 2, sm: 0 },
              fontSize: '0.75rem'
            }}
          >
            {['Privacy Policy', 'Terms of Service', 'Cookies Settings'].map((label) => (
              <Link key={label} href="#" color="text.secondary" underline="hover">
                {label}
              </Link>
            ))}
          </Box>
        </Box>
      </Container>
    </Box>
  );
}
