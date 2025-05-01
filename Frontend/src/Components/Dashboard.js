// src/components/Dashboard.js
import React, { useState, useEffect } from 'react';
import { Box, Tabs, Tab, Paper, useTheme, Typography, Grid, Card, CardContent, CircularProgress } from '@mui/material';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  Legend,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import api from '../Services/api';

// TabPanel helper
function TabPanel({ children, value, index }) {
  return value === index ? <Box sx={{ p: 2 }}>{children}</Box> : null;
}

export default function Dashboard() {
  const theme = useTheme();
  const [tab, setTab] = useState(0);
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        setLoading(true);
        const data = await api.getSavedAnalyses();
        setAnalyses(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch analyses:', err);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyses();
  }, []);

  // Calculate average score
  const averageScore = analyses.length > 0
    ? analyses.reduce((sum, item) => sum + item.score, 0) / analyses.length
    : 0;

  // Create chart data
  const scoreDistributionData = [
    { name: '0-20', count: analyses.filter(a => a.score < 20).length },
    { name: '21-40', count: analyses.filter(a => a.score >= 20 && a.score < 40).length },
    { name: '41-60', count: analyses.filter(a => a.score >= 40 && a.score < 60).length },
    { name: '61-80', count: analyses.filter(a => a.score >= 60 && a.score < 80).length },
    { name: '81-100', count: analyses.filter(a => a.score >= 80).length }
  ];

  // Create timeline data
  const timelineData = analyses.reduce((acc, analysis) => {
    const date = analysis.date.substring(0, 7); // YYYY-MM
    const existing = acc.find(item => item.month === date);
    if (existing) {
      existing.count += 1;
      existing.avgScore = (existing.avgScore * (existing.count - 1) + analysis.score) / existing.count;
    } else {
      acc.push({ month: date, count: 1, avgScore: analysis.score });
    }
    return acc;
  }, []).sort((a, b) => a.month.localeCompare(b.month));

  // Colors for pie chart
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <Paper sx={{ p: 2, borderRadius: 2 }} elevation={1}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Music Analytics Dashboard
      </Typography>
      
      <Tabs
        value={tab}
        onChange={(_, v) => setTab(v)}
        textColor="primary"
        indicatorColor="primary"
        sx={{ mb: 2 }}
      >
        <Tab label="Overview" />
        <Tab label="Score Distribution" />
        <Tab label="Activity Timeline" />
      </Tabs>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Box sx={{ p: 3, textAlign: 'center', color: 'error.main' }}>
          <Typography>{error}</Typography>
        </Box>
      ) : (
        <>
          <TabPanel value={tab} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card elevation={1}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Analysis Summary
                    </Typography>
                    <Typography variant="body1">
                      Total Analyses: {analyses.length}
                    </Typography>
                    <Typography variant="body1">
                      Average Score: {averageScore.toFixed(1)}%
                    </Typography>
                    <Typography variant="body1">
                      High Potential Tracks: {analyses.filter(a => a.score >= 70).length}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card elevation={1}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Score Distribution
                    </Typography>
                    <ResponsiveContainer width="100%" height={200}>
                      <PieChart>
                        <Pie
                          data={scoreDistributionData}
                          dataKey="count"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          outerRadius={80}
                          fill="#8884d8"
                          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                        >
                          {scoreDistributionData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value) => [`${value} tracks`, 'Count']} />
                      </PieChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12}>
                <Card elevation={1}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Recent Activity
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <AreaChart data={timelineData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis yAxisId="left" orientation="left" stroke={theme.palette.primary.main} />
                        <YAxis yAxisId="right" orientation="right" stroke={theme.palette.secondary.main} />
                        <Tooltip />
                        <Legend />
                        <Area
                          yAxisId="left"
                          type="monotone"
                          dataKey="count"
                          stroke={theme.palette.primary.main}
                          fill={theme.palette.primary.light}
                          name="Analyses Count"
                        />
                        <Area
                          yAxisId="right"
                          type="monotone"
                          dataKey="avgScore"
                          stroke={theme.palette.secondary.main}
                          fill={theme.palette.secondary.light}
                          name="Average Score"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={tab} index={1}>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={scoreDistributionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value) => [`${value} tracks`, 'Count']} />
                <Legend />
                <Bar dataKey="count" name="Number of Tracks" fill={theme.palette.primary.main} />
              </BarChart>
            </ResponsiveContainer>
          </TabPanel>
          
          <TabPanel value={tab} index={2}>
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="count"
                  stroke={theme.palette.primary.main}
                  fill={theme.palette.primary.light}
                  name="Number of Analyses"
                />
                <Area
                  type="monotone"
                  dataKey="avgScore"
                  stroke={theme.palette.secondary.main}
                  fill={theme.palette.secondary.light}
                  name="Average Score"
                />
              </AreaChart>
            </ResponsiveContainer>
          </TabPanel>
        </>
      )}
    </Paper>
  );
}