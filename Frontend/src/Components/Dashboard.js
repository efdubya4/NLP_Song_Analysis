// src/Components/Dashboard.js
import React, { useState } from 'react';
import { Box, Tabs, Tab, Paper, useTheme, Typography } from '@mui/material';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';

// Simple mock data
const viralityData = [
  { month: 'Jan', spotify: 45, tiktok: 20 },
  { month: 'Feb', spotify: 50, tiktok: 25 },
  { month: 'Mar', spotify: 55, tiktok: 30 },
  { month: 'Apr', spotify: 60, tiktok: 40 }
];


// const theme = createTheme({
//   palette: {
//     /* … */
//     tertiary: { main: '#6c63ff', light: '#9a95ff', dark: '#3f3acc' },
//     accent:  { main: '#ff4081', light: '#ff79b0', dark: '#c60055' },
//     /* … */
//   }
// });

// TabPanel helper
function TabPanel({ children, value, index }) {
  return value === index ? <Box sx={{ p: 2 }}>{children}</Box> : null;
}

export default function Dashboard() {
  const theme = useTheme();
  const [tab, setTab] = useState(0);

  return (
    <Paper sx={{ p: 2, borderRadius: 2 }} elevation={1}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Music Analytics
      </Typography>

      <Tabs
        value={tab}
        onChange={(_, v) => setTab(v)}
        textColor="primary"
        indicatorColor="primary"
        sx={{ mb: 2 }}
      >
        <Tab label="Overview" />
        <Tab label="Virality Trends" />
      </Tabs>

      <TabPanel value={tab} index={0}>
        <Typography>Welcome to your dashboard!</Typography>
      </TabPanel>

      <TabPanel value={tab} index={1}>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={viralityData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="spotify"
              stroke={theme.palette.primary.main}
              fill={theme.palette.primary.light}
              name="Spotify"
            />
            <Area
              type="monotone"
              dataKey="tiktok"
              stroke={theme.palette.secondary.main}
              fill={theme.palette.secondary.light}
              name="TikTok"
            />
          </AreaChart>
        </ResponsiveContainer>
      </TabPanel>
    </Paper>
  );
}
