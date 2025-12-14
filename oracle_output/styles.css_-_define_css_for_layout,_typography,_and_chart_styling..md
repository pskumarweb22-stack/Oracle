```markdown
# styles.css

## Layout
```css
/* Reset & Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f8f9fa;
    min-height: 100vh;
}

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* Grid System */
.grid {
    display: grid;
    gap: 2rem;
}

.grid-2 {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.grid-3 {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* Flex Utilities */
.flex {
    display: flex;
    gap: 1rem;
}

.flex-col {
    flex-direction: column;
}

.items-center {
    align-items: center;
}

.justify-between {
    justify-content: space-between;
}

/* Spacing */
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }
.mt-8 { margin-top: 2rem; }
.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }

/* Cards */
.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
}

.card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e9ecef;
}

.card-body {
    padding: 1.5rem;
}
```

## Typography
```css
/* Headings */
h1, h2, h3, h4 {
    font-weight: 600;
    line-height: 1.2;
    color: #1a1a1a;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }

/* Text Elements */
p {
    margin-bottom: 1rem;
    color: #555;
}

.lead {
    font-size: 1.125rem;
    color: #666;
}

.text-muted {
    color: #6c757d;
}

.text-center { text-align: center; }
.text-right { text-align: right; }

/* Links */
a {
    color: #0066cc;
    text-decoration: none;
    transition: color 0.2s;
}

a:hover {
    color: #0052a3;
    text-decoration: underline;
}

/* Lists */
ul, ol {
    padding-left: 1.5rem;
    margin-bottom: 1rem;
}

li {
    margin-bottom: 0.5rem;
}

/* Code */
code {
    font-family: 'SFMono-Regular', Consolas, monospace;
    background: #f1f3f5;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-size: 0.9em;
}
```

## Chart Styling
```css
/* Chart Containers */
.chart-container {
    position: relative;
    height: 400px;
    width: 100%;
    margin: 1rem 0;
}

.chart-sm { height: 250px; }
.chart-lg { height: 500px; }

/* Chart Elements */
.chart-tooltip {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    font-size: 0.875rem;
    pointer-events: none;
}

.chart-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1rem;
    justify-content: center;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 2px;
}

/* Axes & Grid */
.chart-axis line,
.chart-axis path {
    stroke: #dee2e6;
    stroke-width: 1;
}

.chart-grid line {
    stroke: #f1f3f5;
    stroke-width: 1;
}

.chart-axis text {
    fill: #6c757d;
    font-size: 0.75rem;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    
    .grid-2,
    .grid-3 {
        grid-template-columns: 1fr;
    }
    
    .chart-container {
        height: 300px;
    }
}
```

## Color Palette
```css
:root {
    --primary: #0066cc;
    --secondary: #6c757d;
    --success: #28a745;
    --danger: #dc3545;
    --warning: #ffc107;
    --info: #17a2b8;
    --light: #f8f9fa;
    --dark: #343a40;
}
```

*Last updated: $(date)*
```