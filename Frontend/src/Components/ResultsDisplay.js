import React from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  LinearProgress,
  Divider,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button
} from '@mui/material';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import EqualizerIcon from '@mui/icons-material/Equalizer';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';

export default function ResultsDisplay({ results, formData }) {
  if (!results) return null;

  const hitProbability = (results.probability_top_chart * 100).toFixed(1);
  const confidenceLevel = (results.confidence * 100).toFixed(1);

  const getScoreColor = (value) => {
    if (value >= 70) return 'success.main';
    if (value >= 40) return 'warning.main';
    return 'error.main';
  };

  const getScoreMessage = (value) => {
    if (value >= 70) return "High hit potential!";
    if (value >= 40) return "Moderate hit potential";
    return "Low hit potential";
  };

  const generateRecommendations = () => {
    const recommendations = [];
    if (formData.danceability < 0.5) {
      recommendations.push("Consider increasing the danceability with a stronger rhythm section");
    }
    if (formData.energy < 0.6) {
      recommendations.push("The track could benefit from higher energy elements like stronger drums or synths");
    } else if (formData.energy > 0.85) {
      recommendations.push("The energy is very high - ensure there are dynamic breaks for contrast");
    }
    if (formData.valence < 0.4 && formData.genre === "Pop") {
      recommendations.push("For pop music, consider a more upbeat emotional tone for wider appeal");
    }
    if (formData.tempo < 90 || formData.tempo > 160) {
      recommendations.push("The tempo is outside the typical range for most hits. Consider adjusting to 100-140 BPM");
    }
    if (recommendations.length === 0) {
      recommendations.push("Your audio features look well-balanced for hit potential!");
    }
    if (formData.lyrics.length < 100) {
      recommendations.push("Add more complete lyrics for a more accurate analysis");
    } else {
      recommendations.push("Consider strong, relatable hooks in the chorus for better audience retention");
    }
    return recommendations;
  };
  
  const recommendations = generateRecommendations();
  
  // Mock charts data
  const similarHits = [
    { name: "Shape of You - Ed Sheeran", score: 89, match: "Danceability, Energy" },
    { name: "Blinding Lights - The Weeknd", score: 84, match: "Tempo, Energy" },
    { name: "Uptown Funk - Mark Ronson, Bruno Mars", score: 78, match: "Genre, Danceability" },
    { name: "Don't Start Now - Dua Lipa", score: 75, match: "Valence, Danceability" },
  ];
  
  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: { xs: 2, md: 4 }, 
        borderRadius: 2, 
        overflow: 'hidden',
        position: 'relative',
        mt: 3
      }}
    >
      <Box sx={{ 
        position: 'absolute', 
        top: 0, 
        right: 0, 
        width: { xs: '100%', md: '30%' }, 
        height: '8px', 
        background: 'linear-gradient(90deg, #ff6d00 0%, #4a148c 100%)' 
      }} />
      
      <Typography variant="h4" gutterBottom sx={{ 
        display: 'flex', 
        alignItems: 'center',
        color: 'primary.main',
        mb: 3 
      }}>
        <EqualizerIcon sx={{ mr: 1, color: 'secondary.main' }} />
        Prediction Results
      </Typography>
      
      <Grid container spacing={4}>
        {/* Main score card */}
        <Grid item xs={12} md={4}>
          <Card 
            elevation={4} 
            sx={{ 
              height: '100%', 
              display: 'flex', 
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              py: 4,
              background: 'linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(245,245,245,1) 100%)',
            }}
          >
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
                width: 140,
                height: 140,
                mb: 2
              }}>
                <Box sx={{ 
                  position: 'absolute',
                  width: '100%',
                  height: '100%',
                  borderRadius: '50%',
                  background: `conic-gradient(${getScoreColor(hitProbability)} ${hitProbability}%, #e0e0e0 0)`,
                  transform: 'rotate(-90deg)',
                }} />
                <Box sx={{ 
                  position: 'absolute',
                  width: '80%',
                  height: '80%',
                  borderRadius: '50%',
                  backgroundColor: 'white',
                }} />
                <Typography variant="h3" sx={{ 
                  fontWeight: 'bold',
                  color: getScoreColor(hitProbability),
                  zIndex: 1
                }}>
                  {hitProbability}%
                </Typography>
              </Box>
              
              <Chip 
                label={getScoreMessage(hitProbability)} 
                color={
                  hitProbability >= 70 ? "success" : 
                  hitProbability >= 40 ? "warning" : "error"
                }
                icon={hitProbability >= 50 ? <ThumbUpIcon /> : <ThumbDownIcon />}
                sx={{ fontWeight: 'bold' }}
              />
              
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Confidence: {confidenceLevel}%
              </Typography>
            </Box>
          </Card>
        </Grid>
        
        {/* Feature impact chart */}
        <Grid item xs={12} md={8}>
          <Card elevation={2} sx={{ height: '100%', p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Feature Impact Analysis
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Feature</TableCell>
                    <TableCell>Value</TableCell>
                    <TableCell>Impact</TableCell>
                    <TableCell>Contribution</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>Danceability</TableCell>
                    <TableCell>{formData.danceability.toFixed(2)}</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {results.analysis.danceability_impact > 20 ? 
                          <TrendingUpIcon color="success" fontSize="small" sx={{ mr: 1 }} /> :
                          <TrendingDownIcon color="error" fontSize="small" sx={{ mr: 1 }} />
                        }
                        {results.analysis.danceability_impact.toFixed(1)}%
                      </Box>
                    </TableCell>
                    <TableCell>
                      <LinearProgress 
                        variant="determinate" 
                        value={results.analysis.danceability_impact} 
                        color={results.analysis.danceability_impact > 20 ? "success" : "error"}
                        sx={{ height: 10, borderRadius: 5 }}
                      />
                    </TableCell>
                  </TableRow>
                  
                  <TableRow>
                    <TableCell>Energy</TableCell>
                    <TableCell>{formData.energy.toFixed(2)}</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {results.analysis.energy_impact > 20 ? 
                          <TrendingUpIcon color="success" fontSize="small" sx={{ mr: 1 }} /> :
                          <TrendingDownIcon color="error" fontSize="small" sx={{ mr: 1 }} />
                        }
                        {results.analysis.energy_impact.toFixed(1)}%
                      </Box>
                    </TableCell>
                    <TableCell>
                      <LinearProgress 
                        variant="determinate" 
                        value={results.analysis.energy_impact} 
                        color={results.analysis.energy_impact > 20 ? "success" : "error"}
                        sx={{ height: 10, borderRadius: 5 }}
                      />
                    </TableCell>
                  </TableRow>
                  
                  <TableRow>
                    <TableCell>Valence</TableCell>
                    <TableCell>{formData.valence.toFixed(2)}</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {results.analysis.valence_impact > 20 ? 
                          <TrendingUpIcon color="success" fontSize="small" sx={{ mr: 1 }} /> :
                          <TrendingDownIcon color="error" fontSize="small" sx={{ mr: 1 }} />
                        }
                        {results.analysis.valence_impact.toFixed(1)}%
                      </Box>
                    </TableCell>
                    <TableCell>
                      <LinearProgress 
                        variant="determinate" 
                        value={results.analysis.valence_impact} 
                        color={results.analysis.valence_impact > 20 ? "success" : "error"}
                        sx={{ height: 10, borderRadius: 5 }}
                      />
                    </TableCell>
                  </TableRow>
                  
                  <TableRow>
                    <TableCell>Tempo</TableCell>
                    <TableCell>{formData.tempo.toFixed(0)} BPM</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {results.analysis.tempo_impact > 10 ? 
                          <TrendingUpIcon color="success" fontSize="small" sx={{ mr: 1 }} /> :
                          <TrendingDownIcon color="error" fontSize="small" sx={{ mr: 1 }} />
                        }
                        {results.analysis.tempo_impact.toFixed(1)}%
                      </Box>
                    </TableCell>
                    <TableCell>
                      <LinearProgress 
                        variant="determinate" 
                        value={results.analysis.tempo_impact} 
                        color={results.analysis.tempo_impact > 10 ? "success" : "error"}
                        sx={{ height: 10, borderRadius: 5 }}
                      />
                    </TableCell>
                  </TableRow>
                  
                  <TableRow>
                    <TableCell>Lyrics</TableCell>
                    <TableCell>{formData.lyrics.split(/\s+/).filter(Boolean).length} words</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {results.analysis.lyrics_impact > 15 ? 
                          <TrendingUpIcon color="success" fontSize="small" sx={{ mr: 1 }} /> :
                          <TrendingDownIcon color="error" fontSize="small" sx={{ mr: 1 }} />
                        }
                        {results.analysis.lyrics_impact.toFixed(1)}%
                      </Box>
                    </TableCell>
                    <TableCell>
                      <LinearProgress 
                        variant="determinate" 
                        value={results.analysis.lyrics_impact} 
                        color={results.analysis.lyrics_impact > 15 ? "success" : "error"}
                        sx={{ height: 10, borderRadius: 5 }}
                      />
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Card>
        </Grid>
        
        {/* Recommendations */}
        <Grid item xs={12} md={6}>
          <Card elevation={2} sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <MusicNoteIcon sx={{ mr: 1, color: 'primary.main' }} />
                Recommendations
              </Typography>
              
              <Box component="ul" sx={{ pl: 2 }}>
                {recommendations.map((rec, index) => (
                  <Typography component="li" key={index} sx={{ mb: 1 }}>
                    {rec}
                  </Typography>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Similar hits */}
        <Grid item xs={12} md={6}>
          <Card elevation={2} sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUpIcon sx={{ mr: 1, color: 'primary.main' }} />
                Similar Hit Songs
              </Typography>
              
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Song</TableCell>
                      <TableCell>Match</TableCell>
                      <TableCell align="right">Score</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {similarHits.map((hit, index) => (
                      <TableRow key={index}>
                        <TableCell>{hit.name}</TableCell>
                        <TableCell>{hit.match}</TableCell>
                        <TableCell align="right">
                          <Chip 
                            size="small" 
                            label={`${hit.score}%`} 
                            color={hit.score > 80 ? "success" : "primary"}
                            variant="outlined"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      <Divider sx={{ my: 4 }} />

      <Box sx={{ display: 'flex', justifyContent: 'center' }}>
        <Button 
          variant="contained" 
          color="secondary"
          startIcon={<MusicNoteIcon />}
          sx={{ 
            mr: 2,
            borderRadius: 3,
            background: 'linear-gradient(to right, #a1c4fd, #c2e9fb)',
            boxShadow: '0 3px 12px rgba(161, 196, 253, 0.3)'
          }}
        >
          Save Analysis
        </Button>
        <Button 
          variant="outlined" 
          color="primary"
          sx={{ 
            borderRadius: 3,
            px: 3,
            borderColor: 'primary.light'
          }}
        >
          Compare With Other Songs
        </Button>
      </Box>
    </Paper>
  );
}