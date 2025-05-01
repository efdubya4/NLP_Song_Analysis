import React, { useState } from 'react';
import { useTheme, alpha } from '@mui/material';
import { 
  Box, 
  Typography, 
  Grid, 
  Paper, 
  Slider, 
  TextField,
  Button,
  CircularProgress,
  Divider,
  Chip,
  Tab,
  Tabs,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tooltip,
  IconButton,
  Card,
  CardContent,
  Stack,
  LinearProgress,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import EqualizerIcon from '@mui/icons-material/Equalizer';
import QueueMusicIcon from '@mui/icons-material/QueueMusic';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import VerifiedIcon from '@mui/icons-material/Verified';
import LibraryMusicIcon from '@mui/icons-material/LibraryMusic';
import HeadphonesIcon from '@mui/icons-material/Headphones';
import MusicVideoIcon from '@mui/icons-material/MusicVideo';
import TuneIcon from '@mui/icons-material/Tune';
import SpeedIcon from '@mui/icons-material/Speed';
import MoodIcon from '@mui/icons-material/Mood';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';

// Mock function to simulate prediction (since we're ignoring backend)
const mockPredictHit = (formData) => {
  // Simulate API delay
  return new Promise((resolve) => {
    setTimeout(() => {
      // Create prediction based on form values
      const danceabilityFactor = formData.danceability * 0.3;
      const energyFactor = formData.energy * 0.25;
      const valenceFactor = formData.valence * 0.2;
      const tempoFactor = (formData.tempo - 50) / 150 * 0.15; // Normalize tempo to 0-1
      
      // Generate random factor for lyrics (would be analyzed by backend)
      const lyricsFactor = formData.lyrics.length > 50 ? Math.random() * 0.2 : 0.05;
      
      // Calculate probability (make it look realistic)
      let probability = danceabilityFactor + energyFactor + valenceFactor + tempoFactor + lyricsFactor;
      
      // Add a random factor to make it more realistic
      probability = Math.min(0.95, Math.max(0.05, probability + (Math.random() * 0.2 - 0.1)));
      
      // Create mock confidence based on lyrics length
      const confidence = Math.min(0.9, 0.5 + (formData.lyrics.length / 1000));
      
      resolve({
        probability_top_chart: probability,
        confidence: confidence,
        analysis: {
          danceability_impact: danceabilityFactor / probability * 100,
          energy_impact: energyFactor / probability * 100,
          valence_impact: valenceFactor / probability * 100,
          tempo_impact: tempoFactor / probability * 100,
          lyrics_impact: lyricsFactor / probability * 100
        }
      });
    }, 1500); // Simulate 1.5s delay
  });
};

// Feature info tooltips
const featureInfos = {
  danceability: "How suitable a track is for dancing based on tempo, rhythm stability, beat strength, and overall regularity. 0.0 is least danceable and 1.0 is most danceable.",
  energy: "A measure of intensity and activity. Energetic tracks feel fast, loud, and noisy. 0.0 is low energy, 1.0 is high energy.",
  valence: "A measure of musical positiveness. Tracks with high valence (1.0) sound more positive (happy, cheerful), while tracks with low valence (0.0) sound more negative (sad, angry).",
  tempo: "The overall estimated tempo of a track in beats per minute (BPM)."
};

// Genre list for select dropdown
const genres = [
  "Pop", "Hip Hop", "Rock", "R&B", "Country", 
  "Electronic", "Jazz", "Classical", "Reggae", 
  "Folk", "Metal", "Blues", "Latin", "Alternative", "K-Pop"
];


export default function SongForm() {
  const theme = useTheme();
  const [activeTab, setActiveTab] = useState(0);
  const [formData, setFormData] = useState({
    danceability: 0.65,
    energy: 0.7,
    tempo: 120,
    valence: 0.6,
    lyrics: "",
    genre: "Pop"
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [analysisStarted, setAnalysisStarted] = useState(false);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleSliderChange = (field) => (event, newValue) => {
    setFormData({...formData, [field]: newValue});
  };

  const handleInputChange = (field) => (event) => {
    setFormData({...formData, [field]: event.target.value});
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setAnalysisStarted(true);
    
    try {
      // Use mock prediction function (would be API call to backend)
      const prediction = await mockPredictHit(formData);
      setResults(prediction);
    } catch (error) {
      console.error("Error predicting hit:", error);
      // In a real app, would handle error state here
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      danceability: 0.65,
      energy: 0.7,
      tempo: 120,
      valence: 0.6,
      lyrics: "",
      genre: "Pop"
    });
    setResults(null);
    setAnalysisStarted(false);
  };

  // Get score color based on percentage
  const getScoreColor = (value) => {
    if (value >= 70) return 'success.main';
    if (value >= 40) return 'warning.main';
    return 'error.main';
  };

  // Music trends cards
  const trendCards = [
    {
      title: "High Energy",
      icon: <TrendingUpIcon />,
      description: "Uptempo, high energy tracks are trending in the charts",
      value: 87
    },
    {
      title: "Positive Vibe",
      icon: <MoodIcon />,
      description: "Songs with higher valence scores are more likely to chart",
      value: 74
    },
    {
      title: "Strong Rhythm",
      icon: <HeadphonesIcon />,
      description: "Danceable tracks have increased success probability",
      value: 82
    }
  ];

  return (
    <Box>
      {/* Welcome message section */}
      {!analysisStarted && (
        <Paper 
          elevation={0} 
          sx={{ 
            p: 4, 
            mb: 4, 
            borderRadius: 3,
            backgroundImage: 'linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)',
            border: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography 
                variant="h3" 
                component="h1" 
                gutterBottom
                sx={{ 
                  fontWeight: 800,
                  background: 'linear-gradient(to right, #a1c4fd, #c2e9fb)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Analyze Your Song's Hit Potential
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph sx={{ fontSize: '1.1rem' }}>
                Use our advanced AI algorithm to predict your song's commercial success potential. 
                Adjust audio features and enter lyrics to get personalized insights.
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <VerifiedIcon sx={{ color: 'primary.main', mr: 1 }} />
                <Typography variant="body1" color="text.primary" fontWeight={500}>
                  Powered by data from thousands of hit songs
                </Typography>
              </Box>
              <Box sx={{ mt: 3 }}>
                <Button 
                  variant="contained"
                  color="primary"
                  size="large"
                  onClick={() => setAnalysisStarted(true)}
                  startIcon={<MusicNoteIcon />}
                  sx={{ 
                    mr: 2,
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #f6d365, #fda085)',
                    boxShadow: '0 4px 14px rgba(253, 160, 133, 0.3)' 
                  }}
                >
                  Start New Analysis
                </Button>
                <Button 
                  variant="outlined"
                  color="primary"
                  size="large"
                  startIcon={<SupportAgentIcon />}
                  sx={{ borderRadius: 2 }}
                >
                  How It Works
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12} md={5}>
            </Grid>
          </Grid>
        </Paper>
      )}
      {/* Music trends section */}
      {!analysisStarted && (
        <Box sx={{ mb: 5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <TrendingUpIcon sx={{ color: 'primary.main', mr: 1.5, fontSize: 28 }} />
            <Typography variant="h4" sx={{ fontWeight: 600 }}>
              Current Music Trends
            </Typography>
          </Box>
          
          <Grid container spacing={3}>
            {trendCards.map((card, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card 
                  elevation={0}
                  className="card-hover"
                  sx={{ 
                    height: '100%',
                    borderRadius: 3,
                    border: '1px solid',
                    borderColor: 'divider',
                    overflow: 'visible',
                    position: 'relative'
                  }}
                >
                  <Box 
                    sx={{ 
                      position: 'absolute',
                      top: -20,
                      left: 20,
                      width: 56,
                      height: 56,
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: 'primary.main',
                      color: 'white',
                      boxShadow: '0 4px 14px rgba(58, 54, 224, 0.3)'
                    }}
                  >
                    {card.icon}
                  </Box>
                  <CardContent sx={{ pt: 5, pb: 3 }}>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      {card.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {card.description}
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2" color="text.secondary">Trend strength</Typography>
                        <Typography variant="body2" color="primary.main" fontWeight={600}>
                          {card.value}%
                        </Typography>
                      </Box>
                      <LinearProgress 
                        variant="determinate" 
                        value={card.value} 
                        color="primary" 
                        sx={{ height: 6, borderRadius: 3 }}
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Main form */}
      {analysisStarted && (
        <Paper 
          elevation={0} 
          sx={{ 
            p: { xs: 2, md: 4 }, 
            borderRadius: 3,
            border: '1px solid',
            borderColor: 'divider',
            position: 'relative',
            overflow: 'hidden'
          }}
          className="hover-lift"
        >
          <Box sx={{ 
            position: 'absolute', 
            top: 0, 
            left: 0, 
            right: 0, 
            height: '6px', 
            background: 'linear-gradient(90deg, #3a36e0, #ff6b6b)' 
          }} />

          <Typography 
            variant="h4" 
            gutterBottom 
            sx={{ 
              display: 'flex', 
              alignItems: 'center',
              fontWeight: 700,
              mb: 3
            }}
            className="gradient-text"
          >
            <MusicNoteIcon sx={{ mr: 1.5, color: 'primary.main' }} />
            Song Hit Potential Analyzer
          </Typography>

          <Tabs 
            value={activeTab} 
            onChange={handleTabChange} 
            variant="fullWidth" 
            sx={{ 
              mb: 4,
              '& .MuiTab-root': {
                fontWeight: 600,
                py: 1.5
              },
              '& .Mui-selected': {
                color: 'primary.main'
              },
              '& .MuiTabs-indicator': {
                height: 3,
                borderRadius: 1.5
              }
            }}
          >
            <Tab 
              icon={<EqualizerIcon />} 
              label="Audio Features" 
              iconPosition="start"
            />
            <Tab 
              icon={<QueueMusicIcon />} 
              label="Lyrics" 
              iconPosition="start"
            />
          </Tabs>

          <form onSubmit={handleSubmit}>
            {activeTab === 0 && (
              <Box sx={{ mt: 2 }}>
                <Grid container spacing={4}>
                  <Grid item xs={12} md={6}>
                    <Card 
                      elevation={0} 
                      sx={{ 
                        mb: 3, 
                        p: 2, 
                        border: '1px solid',
                        borderColor: 'divider',
                        borderRadius: 2
                      }}
                    >
                      <Typography 
                        variant="subtitle1" 
                        fontWeight={600} 
                        sx={{ 
                          display: 'flex', 
                          alignItems: 'center',
                          mb: 2
                        }}
                      >
                        <LibraryMusicIcon sx={{ mr: 1, color: 'primary.main' }} />
                        Genre Selection
                      </Typography>
                      
                      <FormControl fullWidth variant="outlined">
                        <InputLabel id="genre-label">Genre</InputLabel>
                        <Select
                          labelId="genre-label"
                          value={formData.genre}
                          label="Genre"
                          onChange={handleInputChange('genre')}
                          sx={{ borderRadius: 2 }}
                        >
                          {genres.map((genre) => (
                            <MenuItem key={genre} value={genre}>{genre}</MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Card>
                    
                    <Box 
                      sx={{ 
                        p: 3, 
                        borderRadius: 2, 
                        bgcolor: alpha('#3a36e0', 0.04),
                        border: '1px solid',
                        borderColor: alpha('#3a36e0', 0.1),
                        mb: 3
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <TuneIcon sx={{ mr: 1, color: 'primary.main' }} />
                        <Typography variant="subtitle1" fontWeight={600}>
                          Danceability: {formData.danceability.toFixed(2)}
                        </Typography>
                        <Tooltip title={featureInfos.danceability}>
                          <IconButton size="small" sx={{ ml: 1 }}>
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                      <Slider
                        value={formData.danceability}
                        onChange={handleSliderChange('danceability')}
                        step={0.01}
                        min={0}
                        max={1}
                        marks={[
                          { value: 0, label: 'Low' },
                          { value: 0.5, label: 'Medium' },
                          { value: 1, label: 'High' }
                        ]}
                        sx={{ 
                          color: 'primary.main',
                          '& .MuiSlider-thumb': {
                            width: 24,
                            height: 24,
                            backgroundColor: '#fff',
                            border: '2px solid currentColor',
                            '&:focus, &:hover, &.Mui-active, &.Mui-focusVisible': {
                              boxShadow: '0px 0px 0px 8px rgba(58, 54, 224, 0.16)'
                            }
                          }
                        }}
                      />
                    </Box>
                    
                    <Box 
                      sx={{ 
                        p: 3, 
                        borderRadius: 2, 
                        bgcolor: alpha('#3a36e0', 0.04),
                        border: '1px solid',
                        borderColor: alpha('#3a36e0', 0.1),
                        mb: 3
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <MusicVideoIcon sx={{ mr: 1, color: 'primary.main' }} />
                        <Typography variant="subtitle1" fontWeight={600}>
                          Energy: {formData.energy.toFixed(2)}
                        </Typography>
                        <Tooltip title={featureInfos.energy}>
                          <IconButton size="small" sx={{ ml: 1 }}>
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                      <Slider
                        value={formData.energy}
                        onChange={handleSliderChange('energy')}
                        step={0.01}
                        min={0}
                        max={1}
                        marks={[
                          { value: 0, label: 'Low' },
                          { value: 0.5, label: 'Medium' },
                          { value: 1, label: 'High' }
                        ]}
                        sx={{ 
                          color: 'primary.main',
                          '& .MuiSlider-thumb': {
                            width: 24,
                            height: 24,
                            backgroundColor: '#fff',
                            border: '2px solid currentColor',
                            '&:focus, &:hover, &.Mui-active, &.Mui-focusVisible': {
                              boxShadow: '0px 0px 0px 8px rgba(58, 54, 224, 0.16)'
                            }
                          }
                        }}
                      />
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Box 
                      sx={{ 
                        p: 3, 
                        borderRadius: 2, 
                        bgcolor: alpha('#3a36e0', 0.04),
                        border: '1px solid',
                        borderColor: alpha('#3a36e0', 0.1),
                        mb: 3
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <MoodIcon sx={{ mr: 1, color: 'primary.main' }} />
                        <Typography variant="subtitle1" fontWeight={600}>
                          Valence: {formData.valence.toFixed(2)}
                        </Typography>
                        <Tooltip title={featureInfos.valence}>
                          <IconButton size="small" sx={{ ml: 1 }}>
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                      <Slider
                        value={formData.valence}
                        onChange={handleSliderChange('valence')}
                        step={0.01}
                        min={0}
                        max={1}
                        marks={[
                          { value: 0, label: 'Negative' },
                          { value: 0.5, label: 'Neutral' },
                          { value: 1, label: 'Positive' }
                        ]}
                        sx={{ 
                          color: 'primary.main',
                          '& .MuiSlider-thumb': {
                            width: 24,
                            height: 24,
                            backgroundColor: '#fff',
                            border: '2px solid currentColor',
                            '&:focus, &:hover, &.Mui-active, &.Mui-focusVisible': {
                              boxShadow: '0px 0px 0px 8px rgba(58, 54, 224, 0.16)'
                            }
                          }
                        }}
                      />
                    </Box>
                    
                    <Box 
                      sx={{ 
                        p: 3, 
                        borderRadius: 2, 
                        bgcolor: alpha('#3a36e0', 0.04),
                        border: '1px solid',
                        borderColor: alpha('#3a36e0', 0.1),
                        mb: 3
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <SpeedIcon sx={{ mr: 1, color: 'primary.main' }} />
                        <Typography variant="subtitle1" fontWeight={600}>
                          Tempo: {formData.tempo.toFixed(0)} BPM
                        </Typography>
                        <Tooltip title={featureInfos.tempo}>
                          <IconButton size="small" sx={{ ml: 1 }}>
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                      <Slider
                        value={formData.tempo}
                        onChange={handleSliderChange('tempo')}
                        step={1}
                        min={60}
                        max={200}
                        marks={[
                          { value: 60, label: '60' },
                          { value: 120, label: '120' },
                          { value: 200, label: '200' }
                        ]}
                        sx={{ 
                          color: 'primary.main',
                          '& .MuiSlider-thumb': {
                            width: 24,
                            height: 24,
                            backgroundColor: '#fff',
                            border: '2px solid currentColor',
                            '&:focus, &:hover, &.Mui-active, &.Mui-focusVisible': {
                              boxShadow: '0px 0px 0px 8px rgba(58, 54, 224, 0.16)'
                            }
                          }
                        }}
                      />
                    </Box>
                    
                    <Box sx={{ p: 3, borderRadius: 2, bgcolor: '#f8f9fa', border: '1px dashed #ccc' }}>
                      <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 2 }}>
                        <InfoIcon fontSize="small" sx={{ mr: 1, verticalAlign: 'middle' }} />
                        Tips for optimal results:
                      </Typography>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        • Be as accurate as possible with audio feature values
                      </Typography>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        • Include complete lyrics for better analysis
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        • Select the closest matching genre for your track
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Box>
            )}
            
            {activeTab === 1 && (
              <Box sx={{ mt: 2 }}>
                <Card 
                  elevation={0} 
                  sx={{ 
                    p: 3, 
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    mb: 3
                  }}
                >
                  <Typography 
                    variant="subtitle1" 
                    fontWeight={600} 
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center',
                      mb: 2
                    }}
                  >
                    <QueueMusicIcon sx={{ mr: 1, color: 'primary.main' }} />
                    Song Lyrics
                  </Typography>
                  
                  <TextField
                    fullWidth
                    multiline
                    rows={10}
                    placeholder="Enter your song lyrics here..."
                    label="Lyrics"
                    variant="outlined"
                    value={formData.lyrics}
                    onChange={handleInputChange('lyrics')}
                    sx={{ mb: 2 }}
                    helperText="The more complete your lyrics, the more accurate the prediction will be."
                  />
                  
                  <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
                    <Chip 
                      label={`Words: ${formData.lyrics.split(/\s+/).filter(Boolean).length}`} 
                      size="small" 
                      color="primary"
                      variant="outlined"
                    />
                    <Chip 
                      label={`Characters: ${formData.lyrics.length}`}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  </Stack>
                </Card>
                
                <Box sx={{ p: 3, borderRadius: 2, bgcolor: '#f8f9fa', border: '1px dashed #ccc' }}>
                  <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 2 }}>
                    <InfoIcon fontSize="small" sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Lyrics Analysis Information:
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Our AI analyzes your lyrics for various factors including theme, sentiment, 
                    repetition, structure, and commercial appeal.
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    For the most accurate results, include your complete lyrics including 
                    verses, chorus, and bridge sections.
                  </Typography>
                </Box>
              </Box>
            )}

            <Divider sx={{ my: 4 }} />
            
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
              <Button 
                variant="outlined" 
                color="primary" 
                onClick={handleReset}
                disabled={loading}
                sx={{ 
                  borderRadius: 2,
                  px: 3
                }}
              >
                Reset
              </Button>
              
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <MusicNoteIcon />}
                sx={{ 
                  px: 4,
                  py: 1.5,
                  borderRadius: 2,
                  fontWeight: 600
                }}
              >
                {loading ? 'Analyzing...' : 'Analyze Hit Potential'}
              </Button>
            </Box>
          </form>
        </Paper>
      )}
      
      {/* Results display */}
      {results && (
        <Paper 
          elevation={0} 
          sx={{ 
            p: { xs: 2, md: 4 }, 
            borderRadius: 3,
            border: '1px solid',
            borderColor: 'divider',
            mt: 4,
            position: 'relative',
            overflow: 'hidden'
          }}
          className="hover-lift"
        >
          <Box sx={{ 
            position: 'absolute', 
            top: 0, 
            left: 0, 
            right: 0, 
            height: '6px', 
            background: 'linear-gradient(90deg, #ff6b6b, #3a36e0)' 
          }} />
          
          <Typography 
            variant="h4" 
            gutterBottom 
            sx={{ 
              display: 'flex', 
              alignItems: 'center',
              fontWeight: 700,
              mb: 3 
            }}
            className="gradient-text"
          >
            <EqualizerIcon sx={{ mr: 1.5 }} />
            Analysis Results
          </Typography>
          
          <Grid container spacing={4}>
            {/* Main score card */}
            <Grid item xs={12} md={4}>
              <Card 
                elevation={0} 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  py: 4,
                  border: '1px solid',
                  borderColor: 'divider',
                  borderRadius: 3,
                  position: 'relative',
                  overflow: 'hidden'
                }}
              >
                <Box 
                  sx={{ 
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    height: '6px',
                    bgcolor: getScoreColor(results.probability_top_chart * 100)
                  }} 
                />
                
                <Box sx={{ 
                  display: 'flex', 
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  textAlign: 'center'
                }}>
                  <Typography variant="h6" color="text.secondary" gutterBottom>
                    Hit Potential Score
                  </Typography>
                  
                  <Box sx={{ 
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: 180,
                    height: 180,
                    mb: 2
                  }}>
                    <Box sx={{ 
                      position: 'absolute',
                      width: '100%',
                      height: '100%',
                      borderRadius: '50%',
                      background: `conic-gradient(${getScoreColor(results.probability_top_chart * 100)} ${results.probability_top_chart * 100}%, #e0e0e0 0)`,
                      transform: 'rotate(-90deg)',
                    }} />
                    <Box sx={{ 
                      position: 'absolute',
                      width: '75%',
                      height: '75%',
                      borderRadius: '50%',
                      backgroundColor: 'white',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: '0px 0px 10px rgba(0,0,0,0.05) inset'
                    }} />
                    <Typography variant="h2" sx={{ 
                      fontWeight: 'bold',
                      color: getScoreColor(results.probability_top_chart * 100),
                      zIndex: 1
                    }}>
                      {(results.probability_top_chart * 100).toFixed(0)}%
                    </Typography>
                  </Box>
                  
                  <Chip 
                    label={results.probability_top_chart * 100 >= 70 ? "High hit potential!" : 
                          results.probability_top_chart * 100 >= 40 ? "Moderate hit potential" : 
                          "Low hit potential"} 
                    color={results.probability_top_chart * 100 >= 70 ? "success" : 
                          results.probability_top_chart * 100 >= 40 ? "warning" : 
                          "error"}
                    icon={results.probability_top_chart * 100 >= 50 ? <ThumbUpIcon /> : <ThumbDownIcon />}
                    sx={{ fontWeight: 'bold', px: 2, py: 2.5, borderRadius: 3 }}
                  />
                  
                  <Box sx={{ mt: 3, display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" color="text.secondary">
                      Confidence Level: 
                    </Typography>
                    <Typography variant="body1" fontWeight="bold" sx={{ ml: 1 }}>
                      {(results.confidence * 100).toFixed(0)}%
                    </Typography>
                  </Box>
                </Box>
              </Card>
            </Grid>
            
            {/* Feature impact chart */}
            <Grid item xs={12} md={8}>
              <Card 
                elevation={0} 
                sx={{ 
                  height: '100%', 
                  p: 3,
                  border: '1px solid',
                  borderColor: 'divider',
                  borderRadius: 3
                }}
              >
                <Typography 
                  variant="h6" 
                  gutterBottom
                  sx={{ 
                    display: 'flex', 
                    alignItems: 'center',
                    fontWeight: 600,
                    mb: 3
                  }}
                >
                  <EqualizerIcon sx={{ mr: 1, color: 'primary.main' }} />
                  Feature Impact Analysis
                </Typography>
                
                <Box sx={{ mb: 4 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <TuneIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="subtitle2" fontWeight={500}>
                      Danceability
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    <Typography variant="subtitle2" fontWeight={600} color={results.analysis.danceability_impact > 20 ? "success.main" : "error.main"}>
                      {results.analysis.danceability_impact.toFixed(1)}%
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={results.analysis.danceability_impact} 
                    color={results.analysis.danceability_impact > 20 ? "success" : "error"}
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                </Box>
                
                <Box sx={{ mb: 4 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <MusicVideoIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="subtitle2" fontWeight={500}>
                      Energy
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    <Typography variant="subtitle2" fontWeight={600} color={results.analysis.energy_impact > 20 ? "success.main" : "error.main"}>
                      {results.analysis.energy_impact.toFixed(1)}%
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={results.analysis.energy_impact} 
                    color={results.analysis.energy_impact > 20 ? "success" : "error"}
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                </Box>
                
                <Box sx={{ mb: 4 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <MoodIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="subtitle2" fontWeight={500}>
                      Valence
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    <Typography variant="subtitle2" fontWeight={600} color={results.analysis.valence_impact > 20 ? "success.main" : "error.main"}>
                      {results.analysis.valence_impact.toFixed(1)}%
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={results.analysis.valence_impact} 
                    color={results.analysis.valence_impact > 20 ? "success" : "error"}
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                </Box>
                
                <Box sx={{ mb: 4 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <SpeedIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="subtitle2" fontWeight={500}>
                      Tempo
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    <Typography variant="subtitle2" fontWeight={600} color={results.analysis.tempo_impact > 10 ? "success.main" : "error.main"}>
                      {results.analysis.tempo_impact.toFixed(1)}%
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={results.analysis.tempo_impact} 
                    color={results.analysis.tempo_impact > 10 ? "success" : "error"}
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                </Box>
                
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <QueueMusicIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="subtitle2" fontWeight={500}>
                      Lyrics
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    <Typography variant="subtitle2" fontWeight={600} color={results.analysis.lyrics_impact > 15 ? "success.main" : "error.main"}>
                      {results.analysis.lyrics_impact.toFixed(1)}%
                    </Typography>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={results.analysis.lyrics_impact} 
                    color={results.analysis.lyrics_impact > 15 ? "success" : "error"}
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                </Box>
              </Card>
            </Grid>
            
            {/* Recommendations */}
            <Grid item xs={12}>
              <Card 
                elevation={0} 
                sx={{ 
                  p: 3,
                  border: '1px solid',
                  borderColor: 'divider',
                  borderRadius: 3
                }}
              >
                <Typography 
                  variant="h6" 
                  gutterBottom 
                  sx={{ 
                    display: 'flex', 
                    alignItems: 'center',
                    fontWeight: 600,
                    mb: 3
                  }}
                >
                  <MusicNoteIcon sx={{ mr: 1, color: 'primary.main' }} />
                  Recommendations to Improve Hit Potential
                </Typography>
                
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Box 
                      sx={{ 
                        p: 2, 
                        borderRadius: 2, 
                        bgcolor: alpha('#3a36e0', 0.04),
                        border: '1px solid',
                        borderColor: alpha('#3a36e0', 0.1),
                        mb: 2
                      }}
                    >
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Audio Features
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {formData.danceability < 0.5 ? 
                          "• Consider increasing the danceability with a stronger rhythm section" : 
                          "• Your danceability score is good for commercial appeal"}
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {formData.energy < 0.6 ? 
                          "• The track could benefit from higher energy elements like stronger drums or synths" : 
                          formData.energy > 0.85 ? 
                          "• The energy is very high - ensure there are dynamic breaks for contrast" :
                          "• Your energy level is well-balanced"}
                      </Typography>
                      <Typography variant="body2">
                        {formData.valence < 0.4 && formData.genre === "Pop" ? 
                          "• For pop music, consider a more upbeat emotional tone for wider appeal" : 
                          "• Your emotional tone (valence) fits well with your selected genre"}
                      </Typography>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Box 
                      sx={{ 
                        p: 2, 
                        borderRadius: 2, 
                        bgcolor: alpha('#ff6b6b', 0.04),
                        border: '1px solid',
                        borderColor: alpha('#ff6b6b', 0.1),
                        mb: 2
                      }}
                    >
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Lyrics & Structure
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {formData.lyrics.length < 100 ? 
                          "• Add more complete lyrics for a more accurate analysis" : 
                          "• Your lyrics have good length for proper analysis"}
                      </Typography>
                      <Typography variant="body2" paragraph>
                        "• Consider strong, relatable hooks in the chorus for better audience retention"
                      </Typography>
                      <Typography variant="body2">
                        {formData.tempo < 90 || formData.tempo > 160 ? 
                          "• The tempo is outside the typical range for most hits. Consider adjusting to 100-140 BPM" : 
                          "• Your tempo is within the optimal range for commercial success"}
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
                
                <Box
   sx={{
     mt: 3,
     p: 3,
     borderRadius: 2,
    bgcolor: results.probability_top_chart * 100 >= 70 ? 
      alpha('success.main', 0.1) : 
      results.probability_top_chart * 100 >= 40 ? 
      alpha('warning.main', 0.1) : 
      alpha('error.main', 0.1),
    bgcolor:
      results.probability_top_chart * 100 >= 70
        ? alpha(theme.palette.success.main, 0.1)
        : results.probability_top_chart * 100 >= 40
        ? alpha(theme.palette.warning.main, 0.1)
        : alpha(theme.palette.error.main, 0.1),
     border: '1px solid',
    borderColor: results.probability_top_chart * 100 >= 70 ? 
      alpha('success.main', 0.3) : 
      results.probability_top_chart * 100 >= 40 ? 
      alpha('warning.main', 0.3) : 
      alpha('error.main', 0.3),
    borderColor:
      results.probability_top_chart * 100 >= 70
        ? alpha(theme.palette.success.main, 0.3)
        : results.probability_top_chart * 100 >= 40
        ? alpha(theme.palette.warning.main, 0.3)
        : alpha(theme.palette.error.main, 0.3),
   }}
 >
                  <Typography 
                    variant="subtitle1" 
                    fontWeight={600} 
                    color={results.probability_top_chart * 100 >= 70 ? 
                      'success.main' : 
                      results.probability_top_chart * 100 >= 40 ? 
                      'warning.main' : 
                      'error.main'
                    }
                    sx={{ mb: 1 }}
                  >
                    {results.probability_top_chart * 100 >= 70 ? 
                      "Your song has high hit potential!" : 
                      results.probability_top_chart * 100 >= 40 ? 
                      "Your song has moderate hit potential" : 
                      "Your song needs improvement to increase hit potential"
                    }
                  </Typography>
                  <Typography variant="body2">
                    {results.probability_top_chart * 100 >= 70 ? 
                      "Focus on professional production and marketing to maximize your song's success. Your audio features and structure align well with current hit trends." : 
                      results.probability_top_chart * 100 >= 40 ? 
                      "With some targeted improvements to the key areas highlighted above, your song could significantly increase its hit potential." : 
                      "Consider revising your song based on our recommendations above. Focus especially on the features with lower impact scores."
                    }
                  </Typography>
                </Box>
              </Card>
            </Grid>
          </Grid>
          
          <Divider sx={{ my: 4 }} />
          
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
            <Button 
              variant="contained" 
              color="primary"
              startIcon={<MusicNoteIcon />}
              sx={{ 
                borderRadius: 2,
                px: 4
              }}
            >
              Save Analysis
            </Button>
            <Button 
              variant="outlined" 
              color="primary"
              onClick={handleReset}
              sx={{ 
                borderRadius: 2,
                px: 4
              }}
            >
              Start New Analysis
            </Button>
          </Box>
        </Paper>
      )}
    </Box>
  );
}