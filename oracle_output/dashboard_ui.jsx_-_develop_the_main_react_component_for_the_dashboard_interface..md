```markdown
# DashboardUI.jsx

## Overview
Main React component implementing the core dashboard interface with modular, responsive layout and real-time data visualization capabilities.

## Component Structure

```jsx
import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Refresh,
  Settings,
  ExpandMore,
  ExpandLess
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

// Sub-components
import MetricCard from './components/MetricCard';
import ChartContainer from './components/ChartContainer';
import DataTable from './components/DataTable';
import QuickActions from './components/QuickActions';
import FilterPanel from './components/FilterPanel';

// Styled Components
const DashboardContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
  backgroundColor: theme.palette.background.default,
  minHeight: '100vh',
}));

const HeaderSection = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  borderRadius: theme.shape.borderRadius * 2,
}));

const ContentGrid = styled(Grid)(({ theme }) => ({
  gap: theme.spacing(3),
}));

// Main Component
const DashboardUI = () => {
  // State Management
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds
  const [expandedView, setExpandedView] = useState({});
  const [filters, setFilters] = useState({
    dateRange: 'last7days',
    metrics: ['revenue', 'users', 'conversion'],
    category: 'all'
  });

  // Data Fetching
  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, refreshInterval);
    return () => clearInterval(interval);
  }, [filters, refreshInterval]);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/dashboard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
      });
      const data = await response.json();
      setDashboardData(data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Event Handlers
  const handleRefresh = () => {
    fetchDashboardData();
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const toggleExpandedView = (widgetId) => {
    setExpandedView(prev => ({
      ...prev,
      [widgetId]: !prev[widgetId]
    }));
  };

  // Render Logic
  if (isLoading && !dashboardData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <DashboardContainer>
      {/* Header */}
      <HeaderSection elevation={1}>
        <Box>
          <Typography variant="h4" fontWeight="bold">
            Performance Dashboard
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Last updated: {dashboardData?.lastUpdated || '--'}
          </Typography>
        </Box>
        <Box display="flex" gap={2}>
          <Tooltip title="Refresh Data">
            <IconButton onClick={handleRefresh}>
              <Refresh />
            </IconButton>
          </Tooltip>
          <Tooltip title="Dashboard Settings">
            <IconButton>
              <Settings />
            </IconButton>
          </Tooltip>
        </Box>
      </HeaderSection>

      {/* Filter Panel */}
      <FilterPanel
        filters={filters}
        onFilterChange={handleFilterChange}
      />

      {/* Quick Actions */}
      <QuickActions />

      {/* Main Content Grid */}
      <ContentGrid container>
        {/* Key Metrics Row */}
        <Grid item xs={12}>
          <Grid container spacing={3}>
            {dashboardData?.metrics?.map((metric, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <MetricCard
                  title={metric.title}
                  value={metric.value}
                  change={metric.change}
                  trend={metric.trend}
                  icon={metric.icon}
                />
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Charts Section */}
        <Grid item xs={12} md={8}>
          <ChartContainer
            data={dashboardData?.charts?.primary}
            type="line"
            title="Performance Trends"
            expanded={expandedView.chart1}
            onToggle={() => toggleExpandedView('chart1')}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <ChartContainer
            data={dashboardData?.charts?.secondary}
            type="donut"
            title="Distribution"
            expanded={expandedView.chart2}
            onToggle={() => toggleExpandedView('chart2')}
          />
        </Grid>

        {/* Data Table */}
        <Grid item xs={12}>
          <DataTable
            data={dashboardData?.tableData}
            columns={dashboardData?.tableColumns}
            pagination
            sortable
          />
        </Grid>
      </ContentGrid>

      {/* Footer */}
      <Box mt={4} pt={2} borderTop={1} borderColor="divider">
        <Typography variant="caption" color="textSecondary">
          Auto-refresh: {refreshInterval / 1000}s interval
        </Typography>
      </Box>
    </DashboardContainer>
  );
};

export default DashboardUI;
```

## Key Features

### 1. **Responsive Layout**
- Material-UI Grid system with breakpoints
- Collapsible/expandable widgets
- Mobile-optimized spacing

### 2. **Data Management**
- Real-time data fetching with configurable intervals
- Filter-driven API calls
- Loading states and error handling

### 3. **Interactive Elements**
- Refresh controls with visual feedback
- Expandable chart views
- Configurable filter panel
- Quick action buttons

### 4. **Performance Optimizations**
- Memoized sub-components
- Efficient re-rendering patterns
- Debounced filter updates

## Props & State

### State Variables
- `dashboardData`: Complete dashboard dataset
- `isLoading`: Data fetching status
- `refreshInterval`: Auto-refresh timing
- `expandedView`: Widget expansion state
- `filters`: Active filter configuration

### Event Handlers
- `fetchDashboardData()`: Data retrieval
- `handleRefresh()`: Manual refresh
- `handleFilterChange()`: Filter updates
- `toggleExpandedView()`: Widget toggling

## Dependencies
- React 18+
- Material-UI v5
- Chart.js (via ChartContainer)
- Custom sub-components

## Usage Example
```jsx
import DashboardUI from './DashboardUI';

function App() {
  return (
    <ThemeProvider theme={customTheme}>
      <CssBaseline />
      <DashboardUI />
    </ThemeProvider>
  );
}
```

## Notes
- All API calls are mockable for development
- Sub-components are independently testable
- Theme customization via Material-UI theme provider
- Accessibility features built-in (ARIA labels, keyboard navigation)
```