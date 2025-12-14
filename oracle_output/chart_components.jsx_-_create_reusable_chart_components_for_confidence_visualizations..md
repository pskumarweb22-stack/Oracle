```markdown
# Chart Components for Confidence Visualizations

## Overview
`chart_components.jsx` provides reusable React components for visualizing confidence intervals and statistical distributions in data dashboards.

## Components

### 1. ConfidenceIntervalChart
Visualizes confidence intervals with customizable error bars.

**Props:**
```jsx
{
  data: Array<{x: number|string, y: number, ci: number}>,
  width: number,
  height: number,
  showPoints: boolean,
  colorScheme: string[],
  xLabel: string,
  yLabel: string
}
```

**Features:**
- Interactive hover tooltips showing exact values
- Responsive error bars with adjustable opacity
- Support for multiple data series

### 2. DistributionChart
Displays probability distributions with confidence shading.

**Props:**
```jsx
{
  distribution: 'normal' | 't' | 'uniform',
  mean: number,
  stdDev: number,
  confidenceLevel: number, // 0.95, 0.99, etc.
  showPercentiles: boolean
}
```

**Features:**
- Animated confidence region transitions
- Vertical lines marking confidence bounds
- Area shading for confidence intervals

### 3. ComparisonChart
Compares multiple confidence intervals side-by-side.

**Props:**
```jsx
{
  groups: Array<{
    label: string,
    mean: number,
    ci: [number, number],
    sampleSize: number
  }>,
  showSignificance: boolean
}
```

**Features:**
- Statistical significance indicators (p < 0.05, etc.)
- Sample size weighting visualization
- Group comparison connectors

## Usage Example

```jsx
import { ConfidenceIntervalChart, DistributionChart } from './chart_components';

const AnalysisDashboard = () => (
  <div className="chart-container">
    <ConfidenceIntervalChart
      data={experimentResults}
      width={600}
      height={400}
      confidenceLevel={0.95}
      showPoints={true}
    />
    <DistributionChart
      distribution="normal"
      mean={42.5}
      stdDev={3.2}
      confidenceLevel={0.99}
    />
  </div>
);
```

## Styling
- Built with CSS-in-JS (emotion/styled-components)
- Theme-aware color schemes
- Consistent typography scale
- Accessible contrast ratios

## Accessibility Features
- ARIA labels for screen readers
- Keyboard navigation support
- High-contrast mode compatibility
- Reduced motion preferences respected

## Dependencies
- React 16.8+
- D3.js (lightweight usage for scales)
- PropTypes for type checking

## Best Practices
1. Always provide meaningful labels
2. Include confidence level in tooltips
3. Use consistent color encoding
4. Provide data source attribution
5. Implement loading states for async data

## Performance
- Memoized component calculations
- Virtualized rendering for large datasets
- Debounced resize handlers
- Efficient SVG rendering
```

This component library provides production-ready chart components specifically designed for statistical confidence visualization, with emphasis on clarity, accuracy, and user interaction.