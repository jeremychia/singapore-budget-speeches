// ===================================
// LANGUAGE ANALYSIS PAGE
// Singapore Budget Speeches (1960-2025)
// Redesigned with better visualizations
// ===================================

let languageData = null;

// Minister chronological order (for sorting)
const ministerOrder = [
  "Goh Keng Swee",
  "Lim Kim San",
  "Hon Sui Sen",
  "Goh Chok Tong",
  "Dr Tony Tan Keng Yam",
  "Dr Richard Hu Tsu Tau",
  "Lee Hsien Loong",
  "Tharman Shanmugaratnam",
  "Heng Swee Keat",
  "Lawrence Wong",
];

// Crisis years for annotations
const CRISIS_YEARS = [
  { year: 1973, label: "Oil Crisis" },
  { year: 1985, label: "1985 Recession" },
  { year: 1997, label: "Asian Financial Crisis" },
  { year: 2003, label: "SARS" },
  { year: 2008, label: "Global Financial Crisis" },
  { year: 2020, label: "COVID-19" },
];

// Minister tenure periods (for shaded regions)
const MINISTER_TENURES = [
  {
    name: "Goh Keng Swee",
    start: 1959,
    end: 1965,
    color: "rgba(12,35,64,0.15)",
  },
  {
    name: "Lim Kim San",
    start: 1965,
    end: 1967,
    color: "rgba(200,16,46,0.15)",
  },
  {
    name: "Goh Keng Swee",
    start: 1967,
    end: 1970,
    color: "rgba(12,35,64,0.15)",
  },
  {
    name: "Hon Sui Sen",
    start: 1970,
    end: 1983,
    color: "rgba(45,106,79,0.15)",
  },
  {
    name: "Goh Chok Tong",
    start: 1983,
    end: 1985,
    color: "rgba(212,167,44,0.15)",
  },
  {
    name: "Dr Tony Tan Keng Yam",
    start: 1985,
    end: 1991,
    color: "rgba(158,162,162,0.15)",
  },
  {
    name: "Dr Richard Hu Tsu Tau",
    start: 1991,
    end: 2001,
    color: "rgba(12,35,64,0.15)",
  },
  {
    name: "Lee Hsien Loong",
    start: 2001,
    end: 2007,
    color: "rgba(200,16,46,0.15)",
  },
  {
    name: "Tharman Shanmugaratnam",
    start: 2007,
    end: 2015,
    color: "rgba(45,106,79,0.15)",
  },
  {
    name: "Heng Swee Keat",
    start: 2015,
    end: 2021,
    color: "rgba(212,167,44,0.15)",
  },
  {
    name: "Lawrence Wong",
    start: 2021,
    end: 2026,
    color: "rgba(158,162,162,0.15)",
  },
];

// Toggle state for each chart
const chartOverlays = {
  vocabulary: { crisis: false, ministers: false },
  temporal: { crisis: false, ministers: false },
  certainty: { crisis: false, ministers: false },
  passive: { crisis: false, ministers: false },
};

// Civic Strength color palette
const colors = {
  primary: "#0C2340", // Deep Navy
  accent: "#C8102E", // Vibrant Red
  success: "#2D6A4F", // Forest Green
  warning: "#D4A72C", // Civic Gold
  neutral: "#9EA2A2", // Slate Gray
  light: "#FAF9F7", // Warm Sand
  grid: "#E2E8F0",
};

// Initialize page
document.addEventListener("DOMContentLoaded", () => {
  loadLanguageData();
});

// Load language statistics
async function loadLanguageData() {
  try {
    const response = await fetch("data/summary/yearly_overview.json");
    languageData = await response.json();

    hideLoading();
    renderMetricsSummary();
    renderInsights();
    renderTrendChart();
    renderCorrelationChart();
    renderMinisterChart();
    renderDecadeChart();
    // New linguistic feature charts
    renderVocabularyChart();
    renderTemporalChart();
    renderCertaintyChart();
    renderPassiveChart();
    // Add overlay toggle controls after charts are rendered
    addChartOverlayControls();
  } catch (error) {
    console.error("Failed to load language data:", error);
    document.getElementById("loading").innerHTML = `
            <p style="color: ${colors.accent};">Failed to load data. Please refresh the page.</p>
        `;
  }
}

// Hide loading state
function hideLoading() {
  document.getElementById("loading").style.display = "none";
  document.getElementById("content").style.display = "block";
}

// Add toggle controls to linguistic charts
function addChartOverlayControls() {
  const charts = ["vocabulary", "temporal", "certainty", "passive"];

  charts.forEach((chartName) => {
    const chartContainer = document
      .getElementById(`${chartName}Chart`)
      .closest(".chart-container");
    const description = chartContainer.querySelector(".chart-description");

    // Create toggle controls container
    const controls = document.createElement("div");
    controls.className = "chart-overlay-controls";
    controls.innerHTML = `
      <span class="overlay-label">Show overlays:</span>
      <label class="overlay-toggle">
        <input type="checkbox" id="${chartName}-crisis" />
        <span class="toggle-text">Crisis Years</span>
      </label>
      <label class="overlay-toggle">
        <input type="checkbox" id="${chartName}-ministers" />
        <span class="toggle-text">Minister Periods</span>
      </label>
    `;

    // Insert after description
    description.insertAdjacentElement("afterend", controls);

    // Create minister legend container (hidden by default)
    const legendDiv = document.createElement("div");
    legendDiv.id = `${chartName}-minister-legend`;
    legendDiv.className = "minister-legend";
    legendDiv.style.display = "none";
    controls.insertAdjacentElement("afterend", legendDiv);

    // Add event listeners
    document
      .getElementById(`${chartName}-crisis`)
      .addEventListener("change", (e) => {
        chartOverlays[chartName].crisis = e.target.checked;
        updateChartOverlays(chartName);
      });

    document
      .getElementById(`${chartName}-ministers`)
      .addEventListener("change", (e) => {
        chartOverlays[chartName].ministers = e.target.checked;
        updateChartOverlays(chartName);
        // Toggle legend visibility
        const legend = document.getElementById(`${chartName}-minister-legend`);
        legend.style.display = e.target.checked ? "flex" : "none";
        if (e.target.checked && !legend.innerHTML) {
          renderMinisterLegend(chartName);
        }
      });
  });
}

// Render minister legend for a chart
function renderMinisterLegend(chartName) {
  const legend = document.getElementById(`${chartName}-minister-legend`);
  // Only show unique ministers (Goh Keng Swee appears twice)
  const uniqueMinisters = [];
  const seenNames = new Set();
  MINISTER_TENURES.forEach((tenure) => {
    if (!seenNames.has(tenure.name)) {
      seenNames.add(tenure.name);
      uniqueMinisters.push(tenure);
    }
  });

  legend.innerHTML = uniqueMinisters
    .map(
      (tenure) => `
      <span class="minister-legend-item">
        <span class="minister-color-box" style="background: ${tenure.color.replace(
          "0.15",
          "0.5",
        )}"></span>
        <span class="minister-name">${tenure.name}</span>
      </span>
    `,
    )
    .join("");
}

// Update chart overlays based on toggle state
function updateChartOverlays(chartName) {
  const chartDiv = document.getElementById(`${chartName}Chart`);
  const currentLayout = chartDiv.layout || {};

  // Get Y-axis range based on chart type
  let yRange;
  switch (chartName) {
    case "vocabulary":
      yRange = [0.1, 0.35];
      break;
    case "temporal":
      yRange = [0.3, 1.0];
      break;
    case "certainty":
      yRange = [0.5, 1.0];
      break;
    case "passive":
      yRange = [0, 45];
      break;
  }

  // Build shapes array
  let shapes = [];

  // Add minister tenure shapes if enabled
  if (chartOverlays[chartName].ministers) {
    shapes = shapes.concat(
      MINISTER_TENURES.map((tenure) => ({
        type: "rect",
        x0: tenure.start.toString(),
        x1: tenure.end.toString(),
        y0: yRange[0],
        y1: yRange[1],
        fillcolor: tenure.color,
        line: { width: 0 },
        layer: "below",
      })),
    );
  }

  // Add crisis lines if enabled
  if (chartOverlays[chartName].crisis) {
    shapes = shapes.concat(
      CRISIS_YEARS.map((crisis) => ({
        type: "line",
        x0: crisis.year.toString(),
        x1: crisis.year.toString(),
        y0: yRange[0],
        y1: yRange[1],
        line: { color: colors.accent, width: 1.5, dash: "dot" },
      })),
    );
  }

  // Add reference line for temporal/certainty charts
  if (
    (chartName === "temporal" || chartName === "certainty") &&
    currentLayout.shapes
  ) {
    // Keep the "balanced" reference line
    const refLine = {
      type: "line",
      x0: "1960",
      x1: "2025",
      y0: 0.5,
      y1: 0.5,
      line: { color: colors.neutral, width: 1, dash: "dash" },
    };
    shapes.push(refLine);
  }

  // Build annotations
  let annotations = [];

  // Add crisis labels if enabled - position them along the line at different heights
  if (chartOverlays[chartName].crisis) {
    const labelPositions = [0.85, 0.75, 0.65, 0.85, 0.75, 0.65]; // Alternate heights
    annotations = annotations.concat(
      CRISIS_YEARS.map((crisis, idx) => {
        // Calculate y position as fraction of range
        const yPos =
          yRange[0] + (yRange[1] - yRange[0]) * labelPositions[idx % 6];
        return {
          x: crisis.year.toString(),
          y: yPos,
          text: crisis.label,
          showarrow: true,
          arrowhead: 0,
          arrowwidth: 1,
          arrowcolor: colors.accent,
          ax: 25,
          ay: 0,
          xanchor: "left",
          font: { size: 9, color: colors.accent },
          bgcolor: "rgba(255,255,255,0.8)",
          borderpad: 2,
        };
      }),
    );
  }

  // Keep original peak/trough annotations
  if (chartName === "vocabulary") {
    annotations.push({
      x: "1976",
      y: 0.291,
      text: "Peak: 1976",
      showarrow: true,
      arrowhead: 2,
      ax: 30,
      ay: -30,
      font: { size: 10, color: colors.primary },
    });
  } else if (chartName === "passive") {
    annotations.push(
      {
        x: "1972",
        y: 37,
        text: "Peak: 1972 (37%)",
        showarrow: true,
        arrowhead: 2,
        ax: 30,
        ay: -30,
        font: { size: 10, color: colors.primary },
      },
      {
        x: "2020",
        y: 4,
        text: "Low: 2020 (4%)",
        showarrow: true,
        arrowhead: 2,
        ax: -30,
        ay: -30,
        font: { size: 10, color: colors.success },
      },
    );
  } else if (chartName === "temporal" || chartName === "certainty") {
    annotations.push({
      x: "2025",
      y: 0.5,
      text: "Balanced",
      showarrow: false,
      xanchor: "right",
      font: { size: 10, color: colors.neutral },
    });
  }

  Plotly.relayout(chartDiv, { shapes: shapes, annotations: annotations });
}

// Render key metrics summary cards
function renderMetricsSummary() {
  const container = document.getElementById("metricsSummary");
  const years = Object.keys(languageData.by_year).sort();

  // Calculate metrics
  const allReadability = years.map((y) => languageData.by_year[y].readability);
  const allSentenceLen = years.map(
    (y) => languageData.by_year[y].avg_sentence_length,
  );

  const earlyYears = years.filter((y) => parseInt(y) < 1980);
  const recentYears = years.filter((y) => parseInt(y) >= 2010);

  const earlyReadability =
    earlyYears.reduce(
      (sum, y) => sum + languageData.by_year[y].readability,
      0,
    ) / earlyYears.length;
  const recentReadability =
    recentYears.reduce(
      (sum, y) => sum + languageData.by_year[y].readability,
      0,
    ) / recentYears.length;

  const earlySentence =
    earlyYears.reduce(
      (sum, y) => sum + languageData.by_year[y].avg_sentence_length,
      0,
    ) / earlyYears.length;
  const recentSentence =
    recentYears.reduce(
      (sum, y) => sum + languageData.by_year[y].avg_sentence_length,
      0,
    ) / recentYears.length;

  const readabilityChange = (
    ((recentReadability - earlyReadability) / earlyReadability) *
    100
  ).toFixed(0);
  const sentenceChange = (
    ((recentSentence - earlySentence) / earlySentence) *
    100
  ).toFixed(0);

  container.innerHTML = `
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">${recentReadability.toFixed(0)}</div>
                <div class="metric-label">Current Readability</div>
                <div class="metric-change positive">+${readabilityChange}% since 1960s</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${recentSentence.toFixed(0)}</div>
                <div class="metric-label">Words per Sentence</div>
                <div class="metric-change ${
                  parseInt(sentenceChange) < 0 ? "positive" : "negative"
                }">${sentenceChange}% since 1960s</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${years.length}</div>
                <div class="metric-label">Speeches Analysed</div>
                <div class="metric-subtitle">1960–2025</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">10</div>
                <div class="metric-label">Finance Ministers</div>
                <div class="metric-subtitle">Compared</div>
            </div>
        </div>
    `;
}

// Render insights from JSON data
function renderInsights() {
  if (!languageData.insights || !Array.isArray(languageData.insights)) return;

  const container = document.getElementById("insights");
  container.innerHTML = languageData.insights
    .map(
      (insight) => `
        <div class="insight-card">
            <h4>${insight.title}</h4>
            <p>${insight.description}</p>
        </div>
    `,
    )
    .join("");
}

// Chart 1: Combined trend chart with smoothed lines
function renderTrendChart() {
  const years = Object.keys(languageData.by_year).sort();
  const readability = years.map((y) => languageData.by_year[y].readability);
  const sentenceLen = years.map(
    (y) => languageData.by_year[y].avg_sentence_length,
  );

  // Calculate 5-year moving average for smoother trends
  const smoothReadability = movingAverage(readability, 5);
  const smoothSentence = movingAverage(sentenceLen, 5);

  const traces = [
    // Raw data as faint markers
    {
      x: years,
      y: readability,
      type: "scatter",
      mode: "markers",
      name: "Readability (raw)",
      marker: { color: colors.primary, size: 6, opacity: 0.3 },
      hovertemplate: "%{x}: %{y:.1f}<extra>Readability</extra>",
    },
    // Smoothed trend line
    {
      x: years,
      y: smoothReadability,
      type: "scatter",
      mode: "lines",
      name: "Readability (trend)",
      line: { color: colors.primary, width: 3 },
      hovertemplate: "%{x}: %{y:.1f}<extra>Readability Trend</extra>",
    },
    // Sentence length on secondary axis
    {
      x: years,
      y: sentenceLen,
      type: "scatter",
      mode: "markers",
      name: "Sentence Length (raw)",
      marker: { color: colors.accent, size: 6, opacity: 0.3 },
      yaxis: "y2",
      hovertemplate: "%{x}: %{y:.1f} words<extra>Sentence Length</extra>",
    },
    {
      x: years,
      y: smoothSentence,
      type: "scatter",
      mode: "lines",
      name: "Sentence Length (trend)",
      line: { color: colors.accent, width: 3 },
      yaxis: "y2",
      hovertemplate: "%{x}: %{y:.1f} words<extra>Sentence Trend</extra>",
    },
  ];

  const layout = {
    xaxis: {
      title: { text: "Year", font: { size: 12 } },
      gridcolor: colors.grid,
      tickmode: "linear",
      dtick: 10,
    },
    yaxis: {
      title: {
        text: "Readability Score",
        font: { size: 12, color: colors.primary },
      },
      range: [30, 80],
      gridcolor: colors.grid,
      tickfont: { color: colors.primary },
    },
    yaxis2: {
      title: {
        text: "Words per Sentence",
        font: { size: 12, color: colors.accent },
      },
      overlaying: "y",
      side: "right",
      range: [35, 10], // Inverted so shorter = higher (better)
      gridcolor: "transparent",
      tickfont: { color: colors.accent },
    },
    height: 450,
    showlegend: true,
    legend: {
      orientation: "h",
      y: -0.15,
      x: 0.5,
      xanchor: "center",
    },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 80, l: 60, r: 60 },
    hovermode: "x unified",
  };

  Plotly.newPlot("trendChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Chart 2: Correlation scatter plot
function renderCorrelationChart() {
  const years = Object.keys(languageData.by_year).sort();

  // Group by minister for coloring
  const ministerData = {};
  years.forEach((year) => {
    const d = languageData.by_year[year];
    const minister = d.minister;
    if (!ministerData[minister]) {
      ministerData[minister] = { x: [], y: [], years: [] };
    }
    ministerData[minister].x.push(d.avg_sentence_length);
    ministerData[minister].y.push(d.readability);
    ministerData[minister].years.push(year);
  });

  const traces = Object.entries(ministerData).map(([minister, data], i) => ({
    x: data.x,
    y: data.y,
    type: "scatter",
    mode: "markers",
    name: minister.replace("Dr ", "").split(" ").slice(0, 2).join(" "),
    marker: {
      size: 12,
      color: getMinisterColor(minister),
      opacity: 0.7,
      line: { color: "white", width: 1 },
    },
    text: data.years,
    hovertemplate: `<b>${minister}</b><br>Year: %{text}<br>Sentence Length: %{x:.1f} words<br>Readability: %{y:.1f}<extra></extra>`,
  }));

  // Add trend line
  const allX = years.map((y) => languageData.by_year[y].avg_sentence_length);
  const allY = years.map((y) => languageData.by_year[y].readability);
  const trendline = linearRegression(allX, allY);

  traces.push({
    x: [Math.min(...allX), Math.max(...allX)],
    y: [
      trendline.predict(Math.min(...allX)),
      trendline.predict(Math.max(...allX)),
    ],
    type: "scatter",
    mode: "lines",
    name: "Trend",
    line: { color: colors.neutral, width: 2, dash: "dash" },
    hoverinfo: "skip",
  });

  const layout = {
    xaxis: {
      title: { text: "Average Sentence Length (words)", font: { size: 12 } },
      gridcolor: colors.grid,
      range: [14, 32],
    },
    yaxis: {
      title: {
        text: "Readability Score (higher = easier)",
        font: { size: 12 },
      },
      gridcolor: colors.grid,
      range: [40, 75],
    },
    height: 450,
    showlegend: true,
    legend: {
      orientation: "h",
      y: -0.2,
      x: 0.5,
      xanchor: "center",
      font: { size: 10 },
    },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 100, l: 60, r: 20 },
    annotations: [
      {
        x: 28,
        y: 45,
        text: "Longer sentences<br>= harder to read",
        showarrow: false,
        font: { size: 11, color: colors.neutral },
      },
      {
        x: 17,
        y: 68,
        text: "Shorter sentences<br>= easier to read",
        showarrow: false,
        font: { size: 11, color: colors.neutral },
      },
    ],
  };

  Plotly.newPlot("correlationChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Chart 3: Minister comparison - horizontal lollipop chart
function renderMinisterChart() {
  const ministers = Object.entries(languageData.by_minister).sort((a, b) => {
    const orderA = ministerOrder.indexOf(a[0]);
    const orderB = ministerOrder.indexOf(b[0]);
    return orderA - orderB;
  });

  const avgReadability =
    ministers.reduce((sum, [_, d]) => sum + d.avg_readability, 0) /
    ministers.length;

  // Create lollipop chart (horizontal bar + marker)
  const traces = [
    // Lines from axis to marker
    {
      x: ministers.map(([_, d]) => d.avg_readability),
      y: ministers.map(([name, _]) => formatMinisterName(name)),
      type: "scatter",
      mode: "markers+text",
      marker: {
        size: 16,
        color: ministers.map(([_, d]) =>
          d.avg_readability >= avgReadability ? colors.success : colors.accent,
        ),
        line: { color: "white", width: 2 },
      },
      text: ministers.map(([_, d]) => d.avg_readability.toFixed(1)),
      textposition: "middle right",
      textfont: { size: 11, color: colors.primary },
      hovertemplate: "%{y}<br>Readability: %{x:.1f}<extra></extra>",
    },
  ];

  // Add horizontal lines (lollipop stems)
  const shapes = ministers.map(([name, d], i) => ({
    type: "line",
    x0: 45,
    x1: d.avg_readability,
    y0: formatMinisterName(name),
    y1: formatMinisterName(name),
    line: {
      color:
        d.avg_readability >= avgReadability ? colors.success : colors.accent,
      width: 3,
    },
  }));

  // Add average line
  shapes.push({
    type: "line",
    x0: avgReadability,
    x1: avgReadability,
    y0: -0.5,
    y1: ministers.length - 0.5,
    line: { color: colors.neutral, width: 2, dash: "dash" },
  });

  const layout = {
    xaxis: {
      title: { text: "Average Readability Score", font: { size: 12 } },
      range: [45, 75],
      gridcolor: colors.grid,
    },
    yaxis: {
      automargin: true,
      tickfont: { size: 11 },
    },
    shapes: shapes,
    height: 450,
    showlegend: false,
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 50, l: 150, r: 50 },
    annotations: [
      {
        x: avgReadability,
        y: ministers.length - 0.3,
        text: `Average: ${avgReadability.toFixed(1)}`,
        showarrow: false,
        font: { size: 10, color: colors.neutral },
        yanchor: "bottom",
      },
    ],
  };

  Plotly.newPlot("ministerChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Chart 4: Decade box plot
function renderDecadeChart() {
  const decades = [
    "1960s",
    "1970s",
    "1980s",
    "1990s",
    "2000s",
    "2010s",
    "2020s",
  ];
  const years = Object.keys(languageData.by_year).sort();

  // Group data by decade - include year labels for hover
  const decadeData = decades.map((decade) => {
    const decadeStart = parseInt(decade);
    const decadeYears = years.filter((y) => {
      const year = parseInt(y);
      return year >= decadeStart && year < decadeStart + 10;
    });
    return {
      values: decadeYears.map((y) => languageData.by_year[y].readability),
      years: decadeYears,
    };
  });

  const traces = decades.map((decade, i) => ({
    y: decadeData[i].values,
    text: decadeData[i].years,
    type: "box",
    name: decade,
    marker: { color: getDecadeColor(i) },
    boxpoints: "all",
    jitter: 0.3,
    pointpos: 0,
    hovertemplate: `<b>%{text}</b><br>Readability: %{y:.1f}<extra></extra>`,
  }));

  const layout = {
    xaxis: {
      title: { text: "Decade", font: { size: 12 } },
    },
    yaxis: {
      title: { text: "Readability Score", font: { size: 12 } },
      range: [35, 80],
      gridcolor: colors.grid,
    },
    height: 400,
    showlegend: false,
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 50, l: 60, r: 20 },
  };

  Plotly.newPlot("decadeChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Utility: Moving average
function movingAverage(data, window) {
  const result = [];
  for (let i = 0; i < data.length; i++) {
    const start = Math.max(0, i - Math.floor(window / 2));
    const end = Math.min(data.length, i + Math.ceil(window / 2));
    const slice = data.slice(start, end);
    result.push(slice.reduce((a, b) => a + b, 0) / slice.length);
  }
  return result;
}

// Utility: Linear regression
function linearRegression(x, y) {
  const n = x.length;
  const sumX = x.reduce((a, b) => a + b, 0);
  const sumY = y.reduce((a, b) => a + b, 0);
  const sumXY = x.reduce((total, xi, i) => total + xi * y[i], 0);
  const sumXX = x.reduce((total, xi) => total + xi * xi, 0);

  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;

  return {
    slope,
    intercept,
    predict: (xi) => slope * xi + intercept,
  };
}

// Utility: Format minister name (full name)
function formatMinisterName(name) {
  return name;
}

// Utility: Get color by minister
function getMinisterColor(name) {
  const idx = ministerOrder.indexOf(name);
  const palette = [
    "#0C2340",
    "#1A3A5C",
    "#2D6A4F",
    "#3D7C8C",
    "#D4A72C",
    "#B45A3C",
    "#6B4E71",
    "#C8102E",
    "#5C5C5C",
    "#9EA2A2",
  ];
  return idx >= 0 ? palette[idx] : colors.neutral;
}

// Utility: Get color by decade index
function getDecadeColor(index) {
  // Gradient from navy to red across decades
  const palette = [
    "#0C2340", // 1960s - Deep Navy
    "#1A3A5C", // 1970s
    "#2D5A7B", // 1980s
    "#3D7C8C", // 1990s
    "#D4A72C", // 2000s - Gold
    "#B45A3C", // 2010s - Terracotta
    "#C8102E", // 2020s - Red
  ];
  return palette[index] || colors.neutral;
}

// ===================================
// CHART 5: VOCABULARY RICHNESS (TTR)
// ===================================
function renderVocabularyChart() {
  const years = Object.keys(languageData.by_year).sort();

  // Check if TTR data exists
  if (!languageData.by_year[years[0]].ttr) {
    document.getElementById("vocabularyChart").innerHTML =
      '<p style="color: #718096; text-align: center; padding: 2rem;">Vocabulary data not available</p>';
    return;
  }

  const ttrData = years.map((y) => languageData.by_year[y].ttr);
  const ministers = years.map((y) => languageData.by_year[y].minister);

  // Build custom hover text with minister and crisis info
  const hoverText = years.map((y, i) => {
    const crisis = CRISIS_YEARS.find((c) => c.year === parseInt(y));
    let text = `<b>${y}</b><br>Minister: ${ministers[i]}<br>TTR: ${ttrData[
      i
    ].toFixed(3)}`;
    if (crisis)
      text += `<br><b style="color:${colors.accent}">⚠ ${crisis.label}</b>`;
    return text;
  });

  // Calculate 5-year moving average
  const movingAvgData = movingAverage(ttrData, 5);

  const traces = [
    {
      x: years,
      y: ttrData,
      name: "Type-Token Ratio",
      type: "scatter",
      mode: "lines+markers",
      line: { color: colors.primary, width: 1.5 },
      marker: { size: 5 },
      hovertemplate: "%{customdata}<extra></extra>",
      customdata: hoverText,
    },
    {
      x: years,
      y: movingAvgData,
      name: "5-Year Average",
      type: "scatter",
      mode: "lines",
      line: { color: colors.accent, width: 2.5 },
      hovertemplate: "<b>%{x}</b><br>5-yr avg: %{y:.3f}<extra></extra>",
    },
  ];

  // No shapes by default - use toggle controls to show overlays
  const layout = {
    xaxis: {
      title: { text: "Year", font: { size: 12 } },
      gridcolor: colors.grid,
      dtick: 10,
    },
    yaxis: {
      title: {
        text: "Type-Token Ratio (unique/total words)",
        font: { size: 12 },
      },
      gridcolor: colors.grid,
      range: [0.1, 0.35],
    },
    shapes: [],
    height: 400,
    showlegend: true,
    legend: { orientation: "h", y: -0.15 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 60, l: 60, r: 20 },
    annotations: [
      {
        x: "1976",
        y: 0.291,
        text: "Peak: 1976",
        showarrow: true,
        arrowhead: 2,
        arrowsize: 1,
        arrowwidth: 1,
        ax: 30,
        ay: -30,
        font: { size: 10, color: colors.primary },
      },
    ],
  };

  Plotly.newPlot("vocabularyChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// ===================================
// CHART 6: TEMPORAL ORIENTATION
// ===================================
function renderTemporalChart() {
  const years = Object.keys(languageData.by_year).sort();

  // Check if temporal data exists
  if (!languageData.by_year[years[0]].temporal_ratio) {
    document.getElementById("temporalChart").innerHTML =
      '<p style="color: #718096; text-align: center; padding: 2rem;">Temporal orientation data not available</p>';
    return;
  }

  const temporalData = years.map((y) => languageData.by_year[y].temporal_ratio);
  const ministers = years.map((y) => languageData.by_year[y].minister);
  const movingAvgData = movingAverage(temporalData, 5);

  // Build custom hover text with minister and crisis info
  const hoverText = years.map((y, i) => {
    const crisis = CRISIS_YEARS.find((c) => c.year === parseInt(y));
    let text = `<b>${y}</b><br>Minister: ${
      ministers[i]
    }<br>Forward ratio: ${temporalData[i].toFixed(2)}`;
    if (crisis)
      text += `<br><b style="color:${colors.accent}">⚠ ${crisis.label}</b>`;
    return text;
  });

  const traces = [
    {
      x: years,
      y: temporalData,
      name: "Forward-Looking Ratio",
      type: "scatter",
      mode: "lines+markers",
      line: { color: colors.success, width: 1.5 },
      marker: { size: 5 },
      hovertemplate: "%{customdata}<extra></extra>",
      customdata: hoverText,
    },
    {
      x: years,
      y: movingAvgData,
      name: "5-Year Average",
      type: "scatter",
      mode: "lines",
      line: { color: colors.accent, width: 2.5 },
      hovertemplate: "<b>%{x}</b><br>5-yr avg: %{y:.2f}<extra></extra>",
    },
  ];

  // Reference line at 0.5 only - crisis lines added via toggle
  const shapes = [
    {
      type: "line",
      x0: years[0],
      x1: years[years.length - 1],
      y0: 0.5,
      y1: 0.5,
      line: { color: colors.neutral, width: 1, dash: "dash" },
    },
  ];

  const layout = {
    xaxis: {
      title: { text: "Year", font: { size: 12 } },
      gridcolor: colors.grid,
      dtick: 10,
    },
    yaxis: {
      title: { text: "Forward-Looking Ratio", font: { size: 12 } },
      gridcolor: colors.grid,
      range: [0.3, 1.0],
    },
    shapes: shapes,
    height: 400,
    showlegend: true,
    legend: { orientation: "h", y: -0.15 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 60, l: 60, r: 20 },
    annotations: [
      {
        x: years[years.length - 1],
        y: 0.5,
        text: "Balanced",
        showarrow: false,
        xanchor: "right",
        font: { size: 10, color: colors.neutral },
      },
    ],
  };

  Plotly.newPlot("temporalChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// ===================================
// CHART 7: CERTAINTY INDEX
// ===================================
function renderCertaintyChart() {
  const years = Object.keys(languageData.by_year).sort();

  // Check if certainty data exists
  if (!languageData.by_year[years[0]].certainty_ratio) {
    document.getElementById("certaintyChart").innerHTML =
      '<p style="color: #718096; text-align: center; padding: 2rem;">Certainty data not available</p>';
    return;
  }

  const certaintyData = years.map(
    (y) => languageData.by_year[y].certainty_ratio,
  );
  const ministers = years.map((y) => languageData.by_year[y].minister);
  const movingAvgData = movingAverage(certaintyData, 5);

  // Build custom hover text with minister and crisis info
  const hoverText = years.map((y, i) => {
    const crisis = CRISIS_YEARS.find((c) => c.year === parseInt(y));
    let text = `<b>${y}</b><br>Minister: ${
      ministers[i]
    }<br>Certainty: ${certaintyData[i].toFixed(2)}`;
    if (crisis)
      text += `<br><b style="color:${colors.accent}">⚠ ${crisis.label}</b>`;
    return text;
  });

  const traces = [
    {
      x: years,
      y: certaintyData,
      name: "Certainty Ratio",
      type: "scatter",
      mode: "lines+markers",
      line: { color: colors.warning, width: 1.5 },
      marker: { size: 5 },
      hovertemplate: "%{customdata}<extra></extra>",
      customdata: hoverText,
    },
    {
      x: years,
      y: movingAvgData,
      name: "5-Year Average",
      type: "scatter",
      mode: "lines",
      line: { color: colors.accent, width: 2.5 },
      hovertemplate: "<b>%{x}</b><br>5-yr avg: %{y:.2f}<extra></extra>",
    },
  ];

  // Reference line at 0.5 only - crisis lines added via toggle
  const shapes = [
    {
      type: "line",
      x0: years[0],
      x1: years[years.length - 1],
      y0: 0.5,
      y1: 0.5,
      line: { color: colors.neutral, width: 1, dash: "dash" },
    },
  ];

  const layout = {
    xaxis: {
      title: { text: "Year", font: { size: 12 } },
      gridcolor: colors.grid,
      dtick: 10,
    },
    yaxis: {
      title: { text: "Certainty Ratio", font: { size: 12 } },
      gridcolor: colors.grid,
      range: [0.5, 1.0],
    },
    shapes: shapes,
    height: 400,
    showlegend: true,
    legend: { orientation: "h", y: -0.15 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 60, l: 60, r: 20 },
    annotations: [
      {
        x: years[years.length - 1],
        y: 0.5,
        text: "Balanced",
        showarrow: false,
        xanchor: "right",
        font: { size: 10, color: colors.neutral },
      },
    ],
  };

  Plotly.newPlot("certaintyChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// ===================================
// CHART 8: PASSIVE VOICE RATIO
// ===================================
function renderPassiveChart() {
  const years = Object.keys(languageData.by_year).sort();

  // Check if passive data exists
  if (!languageData.by_year[years[0]].passive_ratio) {
    document.getElementById("passiveChart").innerHTML =
      '<p style="color: #718096; text-align: center; padding: 2rem;">Passive voice data not available</p>';
    return;
  }

  const passiveData = years.map((y) => languageData.by_year[y].passive_ratio);
  const ministers = years.map((y) => languageData.by_year[y].minister);
  const movingAvgData = movingAverage(passiveData, 5);

  // Build custom hover text with minister and crisis info
  const hoverText = years.map((y, i) => {
    const crisis = CRISIS_YEARS.find((c) => c.year === parseInt(y));
    let text = `<b>${y}</b><br>Minister: ${ministers[i]}<br>Passive: ${(
      passiveData[i] * 100
    ).toFixed(1)}%`;
    if (crisis)
      text += `<br><b style="color:${colors.accent}">⚠ ${crisis.label}</b>`;
    return text;
  });

  const traces = [
    {
      x: years,
      y: passiveData.map((v) => v * 100), // Convert to percentage
      name: "Passive Voice %",
      type: "scatter",
      mode: "lines+markers",
      line: { color: colors.neutral, width: 1.5 },
      marker: { size: 5 },
      hovertemplate: "%{customdata}<extra></extra>",
      customdata: hoverText,
    },
    {
      x: years,
      y: movingAvgData.map((v) => v * 100),
      name: "5-Year Average",
      type: "scatter",
      mode: "lines",
      line: { color: colors.accent, width: 2.5 },
      hovertemplate: "<b>%{x}</b><br>5-yr avg: %{y:.1f}%<extra></extra>",
    },
  ];

  // No shapes by default - use toggle controls to show overlays
  const layout = {
    xaxis: {
      title: { text: "Year", font: { size: 12 } },
      gridcolor: colors.grid,
      dtick: 10,
    },
    yaxis: {
      title: { text: "Passive Voice Usage (%)", font: { size: 12 } },
      gridcolor: colors.grid,
      range: [0, 45],
    },
    shapes: [],
    height: 400,
    showlegend: true,
    legend: { orientation: "h", y: -0.15 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 60, l: 60, r: 20 },
    annotations: [
      {
        x: "1972",
        y: 37,
        text: "Peak: 1972 (37%)",
        showarrow: true,
        arrowhead: 2,
        arrowsize: 1,
        arrowwidth: 1,
        ax: 30,
        ay: -30,
        font: { size: 10, color: colors.primary },
      },
      {
        x: "2020",
        y: 4,
        text: "Low: 2020 (4%)",
        showarrow: true,
        arrowhead: 2,
        arrowsize: 1,
        arrowwidth: 1,
        ax: -30,
        ay: -30,
        font: { size: 10, color: colors.success },
      },
    ],
  };

  Plotly.newPlot("passiveChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}
