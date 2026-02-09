// ===================================
// MINISTERS PAGE - REDESIGNED
// Singapore Budget Speeches (1960-2025)
// Better visualizations for minister comparison
// ===================================

let ministerData = null;

// Chronological order of ministers (source of truth from speech_links.py)
// Portrait images - placeholder for now, to be updated with actual images
const ministerOrder = [
  {
    name: "Goh Keng Swee",
    start: 1960,
    end: 1970,
    era: "founding",
    image: "https://placehold.co/220x280/0C2340/white?text=GKS",
  },
  {
    name: "Lim Kim San",
    start: 1966,
    end: 1967,
    era: "founding",
    image: "https://placehold.co/220x280/0C2340/white?text=LKS",
  },
  {
    name: "Hon Sui Sen",
    start: 1971,
    end: 1978,
    era: "growth",
    image: "https://placehold.co/220x280/2D6A4F/white?text=HSS",
  },
  {
    name: "Goh Chok Tong",
    start: 1979,
    end: 1981,
    era: "growth",
    image: "https://placehold.co/220x280/2D6A4F/white?text=GCT",
  },
  {
    name: "Dr Tony Tan Keng Yam",
    start: 1982,
    end: 1985,
    era: "growth",
    image: "https://placehold.co/220x280/2D6A4F/white?text=TT",
  },
  {
    name: "Dr Richard Hu Tsu Tau",
    start: 1986,
    end: 2001,
    era: "maturity",
    image: "https://placehold.co/220x280/D4A72C/white?text=RH",
  },
  {
    name: "Lee Hsien Loong",
    start: 2002,
    end: 2006,
    era: "maturity",
    image: "https://placehold.co/220x280/D4A72C/white?text=LHL",
  },
  {
    name: "Tharman Shanmugaratnam",
    start: 2007,
    end: 2015,
    era: "modern",
    image: "https://placehold.co/220x280/C8102E/white?text=TS",
  },
  {
    name: "Heng Swee Keat",
    start: 2016,
    end: 2021,
    era: "modern",
    image: "https://placehold.co/220x280/C8102E/white?text=HSK",
  },
  {
    name: "Lawrence Wong",
    start: 2022,
    end: 2025,
    era: "modern",
    image: "https://placehold.co/220x280/C8102E/white?text=LW",
  },
];

// Era colors
const eraColors = {
  founding: "#0C2340", // Deep Navy - Independence era
  growth: "#2D6A4F", // Forest Green - Growth era
  maturity: "#D4A72C", // Gold - Maturity era
  modern: "#C8102E", // Red - Modern era
};

// Civic Strength palette
const colors = {
  primary: "#0C2340",
  accent: "#C8102E",
  success: "#2D6A4F",
  warning: "#D4A72C",
  neutral: "#9EA2A2",
  grid: "#E2E8F0",
};

// Initialize page
document.addEventListener("DOMContentLoaded", () => {
  loadMinisterData();
});

// Load minister statistics
async function loadMinisterData() {
  try {
    const response = await fetch("data/summary/ministers_overview.json");
    ministerData = await response.json();

    // Sort ministers chronologically
    ministerData.ministers = sortMinistersChronologically(
      ministerData.ministers,
    );

    hideLoading();
    renderMetricsSummary();
    renderTimelineChart();
    renderOutputChart();
    renderStyleChart();
    renderTopicsHeatmap();
    renderMinisterProfiles();
  } catch (error) {
    console.error("Failed to load minister data:", error);
    document.getElementById("loading").innerHTML = `
            <p style="color: ${colors.accent};">Failed to load data. Please refresh the page.</p>
        `;
  }
}

// Sort ministers in chronological order
function sortMinistersChronologically(ministers) {
  return ministers.sort((a, b) => {
    const orderA = ministerOrder.findIndex((m) => m.name === a.name);
    const orderB = ministerOrder.findIndex((m) => m.name === b.name);
    return orderA - orderB;
  });
}

// Hide loading state
function hideLoading() {
  document.getElementById("loading").style.display = "none";
  document.getElementById("content").style.display = "block";
}

// Get minister info from order list
function getMinisterInfo(name) {
  return (
    ministerOrder.find((m) => m.name === name) || {
      start: 1960,
      end: 1965,
      era: "founding",
      image: "",
    }
  );
}

// Format minister name (shorter)
function shortName(name) {
  return name
    .replace("Dr ", "")
    .replace(" Tsu Tau", "")
    .replace(" Keng Yam", "");
}

// Render key metrics summary
function renderMetricsSummary() {
  const container = document.getElementById("metricsSummary");
  const ministers = ministerData.ministers;

  const totalSentences = ministers.reduce(
    (sum, m) => sum + m.total_sentences,
    0,
  );
  const totalSpeeches = ministers.reduce((sum, m) => sum + m.num_speeches, 0);
  const avgReadability =
    ministers.reduce((sum, m) => sum + m.readability_score, 0) /
    ministers.length;
  const longestServing = ministers.reduce((a, b) =>
    a.num_speeches > b.num_speeches ? a : b,
  );

  container.innerHTML = `
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">10</div>
                <div class="metric-label">Finance Ministers</div>
                <div class="metric-subtitle">1960–2025</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${totalSpeeches}</div>
                <div class="metric-label">Budget Speeches</div>
                <div class="metric-subtitle">66 years</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${(totalSentences / 1000).toFixed(
                  0,
                )}k</div>
                <div class="metric-label">Total Sentences</div>
                <div class="metric-subtitle">Analysed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${avgReadability.toFixed(0)}</div>
                <div class="metric-label">Avg Readability</div>
                <div class="metric-subtitle">Flesch score</div>
            </div>
        </div>
    `;
}

// Chart 1: Gantt-style timeline
function renderTimelineChart() {
  const ministers = ministerData.ministers;

  // Create Gantt bars
  const traces = ministers.map((minister, i) => {
    const info = getMinisterInfo(minister.name);
    return {
      x: [info.end - info.start],
      y: [shortName(minister.name)],
      type: "bar",
      orientation: "h",
      base: [info.start],
      name: minister.name,
      marker: {
        color: eraColors[info.era],
        line: { color: "white", width: 1 },
      },
      text: [`${info.start}–${info.end}`],
      textposition: "inside",
      textfont: { color: "white", size: 11 },
      hovertemplate: `<b>${minister.name}</b><br>${info.start}–${info.end}<br>${minister.num_speeches} speeches<extra></extra>`,
    };
  });

  const layout = {
    xaxis: {
      title: { text: "Year", font: { size: 12 } },
      range: [1958, 2027],
      tickmode: "linear",
      dtick: 10,
      gridcolor: colors.grid,
    },
    yaxis: {
      automargin: true,
      tickfont: { size: 11 },
    },
    height: 400,
    showlegend: false,
    barmode: "stack",
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 50, l: 140, r: 20 },
    annotations: [
      {
        x: 1962,
        y: 10.5,
        text: "<b>Founding Era</b>",
        showarrow: false,
        font: { size: 10, color: eraColors.founding },
      },
      {
        x: 1977,
        y: 10.5,
        text: "<b>Growth Era</b>",
        showarrow: false,
        font: { size: 10, color: eraColors.growth },
      },
      {
        x: 1995,
        y: 10.5,
        text: "<b>Maturity Era</b>",
        showarrow: false,
        font: { size: 10, color: eraColors.maturity },
      },
      {
        x: 2015,
        y: 10.5,
        text: "<b>Modern Era</b>",
        showarrow: false,
        font: { size: 10, color: eraColors.modern },
      },
    ],
  };

  Plotly.newPlot("timelineChart", traces, layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Chart 2: Output comparison (horizontal lollipop)
function renderOutputChart() {
  const ministers = ministerData.ministers;
  const avgSentences =
    ministers.reduce((sum, m) => sum + m.total_sentences, 0) / ministers.length;

  const trace = {
    x: ministers.map((m) => m.total_sentences),
    y: ministers.map((m) => shortName(m.name)),
    type: "scatter",
    mode: "markers+text",
    marker: {
      size: 14,
      color: ministers.map((m) =>
        m.total_sentences >= avgSentences ? colors.success : colors.accent,
      ),
      line: { color: "white", width: 2 },
    },
    text: ministers.map((m) => m.total_sentences.toLocaleString()),
    textposition: "middle right",
    textfont: { size: 10 },
    hovertemplate:
      "%{y}<br>%{x:,} sentences<br>%{customdata} speeches<extra></extra>",
    customdata: ministers.map((m) => m.num_speeches),
  };

  // Create lollipop stems
  const shapes = ministers.map((m) => ({
    type: "line",
    x0: 0,
    x1: m.total_sentences,
    y0: shortName(m.name),
    y1: shortName(m.name),
    line: {
      color: m.total_sentences >= avgSentences ? colors.success : colors.accent,
      width: 3,
    },
  }));

  // Add average line
  shapes.push({
    type: "line",
    x0: avgSentences,
    x1: avgSentences,
    y0: -0.5,
    y1: ministers.length - 0.5,
    line: { color: colors.neutral, width: 2, dash: "dash" },
  });

  const layout = {
    xaxis: {
      title: { text: "Total Sentences", font: { size: 12 } },
      gridcolor: colors.grid,
      range: [0, 10000],
    },
    yaxis: {
      automargin: true,
      tickfont: { size: 11 },
    },
    shapes: shapes,
    height: 400,
    showlegend: false,
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 10, b: 50, l: 140, r: 60 },
    annotations: [
      {
        x: avgSentences,
        y: ministers.length - 0.3,
        text: `Avg: ${Math.round(avgSentences).toLocaleString()}`,
        showarrow: false,
        font: { size: 10, color: colors.neutral },
        yanchor: "bottom",
      },
    ],
  };

  Plotly.newPlot("outputChart", [trace], layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Chart 3: Style scatter plot (readability vs sentence length)
function renderStyleChart() {
  const ministers = ministerData.ministers;

  const trace = {
    x: ministers.map((m) => m.avg_sentence_length),
    y: ministers.map((m) => m.readability_score),
    type: "scatter",
    mode: "markers+text",
    marker: {
      size: ministers.map((m) => Math.sqrt(m.total_sentences) / 2), // Size by output
      color: ministers.map((m) => eraColors[getMinisterInfo(m.name).era]),
      opacity: 0.8,
      line: { color: "white", width: 2 },
    },
    text: ministers.map((m) => shortName(m.name).split(" ")[0]),
    textposition: "top center",
    textfont: { size: 9 },
    hovertemplate:
      "<b>%{customdata}</b><br>Sentence Length: %{x:.1f} words<br>Readability: %{y:.1f}<extra></extra>",
    customdata: ministers.map((m) => m.name),
  };

  // Add quadrant lines at averages
  const avgLen =
    ministers.reduce((sum, m) => sum + m.avg_sentence_length, 0) /
    ministers.length;
  const avgRead =
    ministers.reduce((sum, m) => sum + m.readability_score, 0) /
    ministers.length;

  const layout = {
    xaxis: {
      title: { text: "Avg Sentence Length (words)", font: { size: 12 } },
      gridcolor: colors.grid,
      range: [15, 25],
    },
    yaxis: {
      title: { text: "Readability Score", font: { size: 12 } },
      gridcolor: colors.grid,
      range: [50, 70],
    },
    shapes: [
      // Vertical line at avg sentence length
      {
        type: "line",
        x0: avgLen,
        x1: avgLen,
        y0: 50,
        y1: 70,
        line: { color: colors.grid, width: 1, dash: "dot" },
      },
      // Horizontal line at avg readability
      {
        type: "line",
        x0: 15,
        x1: 25,
        y0: avgRead,
        y1: avgRead,
        line: { color: colors.grid, width: 1, dash: "dot" },
      },
    ],
    height: 400,
    showlegend: false,
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 50, l: 60, r: 20 },
    annotations: [
      {
        x: 16,
        y: 68,
        text: "Clear & Concise",
        showarrow: false,
        font: { size: 10, color: colors.success },
      },
      {
        x: 24,
        y: 52,
        text: "Complex",
        showarrow: false,
        font: { size: 10, color: colors.accent },
      },
    ],
  };

  Plotly.newPlot("styleChart", [trace], layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Chart 4: Topics heatmap
function renderTopicsHeatmap() {
  if (!ministerData.minister_topics) return;

  const ministers = ministerData.ministers.map((m) => m.name);

  // Get all topics and find top 8
  const topicTotals = {};
  ministers.forEach((minister) => {
    const topics = ministerData.minister_topics[minister] || {};
    Object.entries(topics).forEach(([topic, value]) => {
      if (topic !== "General") {
        // Exclude General as it's too dominant
        topicTotals[topic] = (topicTotals[topic] || 0) + value;
      }
    });
  });

  const top8Topics = Object.entries(topicTotals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map((t) => t[0]);

  // Build heatmap data (normalised by minister total)
  const z = ministers.map((minister) => {
    const topics = ministerData.minister_topics[minister] || {};
    const total = Object.values(topics).reduce((sum, v) => sum + v, 0);
    return top8Topics.map((topic) => {
      const value = topics[topic] || 0;
      return total > 0 ? (value / total) * 100 : 0; // Percentage
    });
  });

  const trace = {
    z: z,
    x: top8Topics,
    y: ministers.map((m) => shortName(m)),
    type: "heatmap",
    colorscale: [
      [0, "#FAF9F7"], // Light
      [0.25, "#E8D4A8"], // Cream
      [0.5, "#D4A72C"], // Gold
      [0.75, "#B45A3C"], // Terracotta
      [1, "#C8102E"], // Red
    ],
    showscale: true,
    colorbar: {
      title: { text: "% of<br>sentences", font: { size: 10 } },
      ticksuffix: "%",
      len: 0.8,
    },
    hovertemplate: "<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>",
  };

  const layout = {
    xaxis: {
      tickangle: -45,
      tickfont: { size: 11 },
    },
    yaxis: {
      automargin: true,
      tickfont: { size: 11 },
    },
    height: 450,
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 20, b: 100, l: 140, r: 80 },
  };

  Plotly.newPlot("topicsHeatmap", [trace], layout, {
    responsive: true,
    displayModeBar: false,
  });
}

// Render minister profile cards
function renderMinisterProfiles() {
  const container = document.getElementById("ministerProfiles");
  const ministers = ministerData.ministers;

  // Calculate rankings
  const readabilityRanked = [...ministers].sort(
    (a, b) => b.readability_score - a.readability_score,
  );
  const sentenceRanked = [...ministers].sort(
    (a, b) => a.avg_sentence_length - b.avg_sentence_length,
  );

  container.innerHTML = `
        <h3>Minister Profiles</h3>
        <div class="minister-cards">
            ${ministers
              .map((minister) => {
                const info = getMinisterInfo(minister.name);
                const readRank =
                  readabilityRanked.findIndex((m) => m.name === minister.name) +
                  1;
                const sentRank =
                  sentenceRanked.findIndex((m) => m.name === minister.name) + 1;

                // Get top topics for this minister
                const topics =
                  ministerData.minister_topics[minister.name] || {};
                const topTopics = Object.entries(topics)
                  .filter(([t, v]) => t !== "General")
                  .sort((a, b) => b[1] - a[1])
                  .slice(0, 3)
                  .map(([t]) => t);

                return `
                    <div class="minister-card" style="border-left: 4px solid ${
                      eraColors[info.era]
                    };">
                        <div class="minister-card-header">
                            <div class="minister-portrait">
                                <img src="${info.image}" alt="${
                                  minister.name
                                }" loading="lazy" onerror="this.style.display='none'">
                            </div>
                            <div class="minister-header-text">
                                <h4>${minister.name}</h4>
                                <span class="minister-tenure">${
                                  minister.years_served
                                }</span>
                            </div>
                        </div>

                        <div class="minister-stats-grid">
                            <div class="minister-stat">
                                <span class="stat-value">${
                                  minister.num_speeches
                                }</span>
                                <span class="stat-label">Speeches</span>
                            </div>
                            <div class="minister-stat">
                                <span class="stat-value">${minister.total_sentences.toLocaleString()}</span>
                                <span class="stat-label">Sentences</span>
                            </div>
                            <div class="minister-stat">
                                <span class="stat-value">${minister.readability_score.toFixed(
                                  0,
                                )}</span>
                                <span class="stat-label">Readability</span>
                                <span class="stat-rank ${
                                  readRank <= 3 ? "top" : ""
                                }">#${readRank}</span>
                            </div>
                            <div class="minister-stat">
                                <span class="stat-value">${minister.avg_sentence_length.toFixed(
                                  1,
                                )}</span>
                                <span class="stat-label">Words/Sentence</span>
                                <span class="stat-rank ${
                                  sentRank <= 3 ? "top" : ""
                                }">#${sentRank}</span>
                            </div>
                        </div>

                        ${
                          topTopics.length > 0
                            ? `
                            <div class="minister-topics">
                                <strong>Top Focus:</strong> ${topTopics.join(
                                  " • ",
                                )}
                            </div>
                        `
                            : ""
                        }
                    </div>
                `;
              })
              .join("")}
        </div>
    `;
}
