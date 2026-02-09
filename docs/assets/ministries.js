// ===================================
// MINISTRIES PAGE
// Singapore Budget Speeches (1960-2025)
// ===================================

let ministryData = null;

// Initialize page
document.addEventListener("DOMContentLoaded", () => {
  loadMinistryData();
});

// Load ministry statistics
async function loadMinistryData() {
  try {
    const response = await fetch("data/summary/ministries_overview.json");
    ministryData = await response.json();

    hideLoading();
    renderCharts();
    renderInsights();
    renderDataTable();
  } catch (error) {
    console.error("Failed to load ministry data:", error);
    document.getElementById("loading").innerHTML = `
            <p style="color: var(--color-error);">Failed to load data. Please refresh the page.</p>
        `;
  }
}

// Hide loading state
function hideLoading() {
  document.getElementById("loading").style.display = "none";
  document.getElementById("content").style.display = "block";
}

// Render charts
function renderCharts() {
  renderMinistriesOverTime();
  renderMinistriesByTotal();
}

// Chart 1: Ministry coverage over time
function renderMinistriesOverTime() {
  if (!ministryData.by_year) return;

  // Prepare data for stacked area chart
  const years = Object.keys(ministryData.by_year).sort();
  const ministries = new Set();

  // Collect all ministries
  years.forEach((year) => {
    Object.keys(ministryData.by_year[year]).forEach((ministry) => {
      ministries.add(ministry);
    });
  });

  // Get top 10 ministries by total coverage
  const top10 = Array.from(ministries)
    .map((ministry) => ({
      ministry,
      total: years.reduce(
        (sum, year) => sum + (ministryData.by_year[year][ministry] || 0),
        0,
      ),
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 10)
    .map((m) => m.ministry);

  // Create traces
  const traces = top10.map((ministry) => ({
    x: years,
    y: years.map((year) => ministryData.by_year[year][ministry] || 0),
    name: ministry,
    type: "scatter",
    mode: "lines",
    stackgroup: "one",
    fillcolor: getColorForMinistry(ministry),
    line: { width: 0 },
  }));

  const layout = {
    title: {
      text: "Top 10 Ministries Coverage Over Time",
      font: { size: 18, color: "#0C2340", family: "Public Sans" },
    },
    xaxis: {
      title: "Year",
      gridcolor: "#E2E8F0",
      linecolor: "#E2E8F0",
    },
    yaxis: {
      title: "Number of Sentences",
      gridcolor: "#E2E8F0",
      linecolor: "#E2E8F0",
    },
    hovermode: "x unified",
    showlegend: true,
    legend: { orientation: "h", y: -0.2 },
    height: 500,
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    margin: { t: 60, b: 80, l: 60, r: 20 },
  };

  Plotly.newPlot("ministriesOverTimeChart", traces, layout, {
    responsive: true,
  });
}

// Chart 2: Ministries by total coverage
function renderMinistriesByTotal() {
  if (!ministryData.by_ministry) return;

  // Sort ministries by total
  const sorted = Object.entries(ministryData.by_ministry)
    .sort((a, b) => b[1].total - a[1].total)
    .slice(0, 10);

  const trace = {
    x: sorted.map((m) => m[1].total),
    y: sorted.map((m) => m[0]),
    type: "bar",
    orientation: "h",
    marker: {
      color: sorted.map((_, i) => getColorByIndex(i)),
    },
  };

  const layout = {
    title: {
      text: "Top 10 Ministries by Total Sentence Count (1960-2025)",
      font: { size: 18, color: "#0C2340", family: "Public Sans" },
    },
    xaxis: {
      title: "Total Sentences",
      gridcolor: "#E2E8F0",
      linecolor: "#E2E8F0",
    },
    yaxis: {
      automargin: true,
      gridcolor: "#E2E8F0",
      linecolor: "#E2E8F0",
    },
    height: 500,
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    margin: { t: 60, b: 40, l: 200, r: 20 },
  };

  Plotly.newPlot("ministriesByTotalChart", [trace], layout, {
    responsive: true,
  });
}

// Render insights
function renderInsights() {
  if (!ministryData.insights) return;

  const container = document.getElementById("insights");
  container.innerHTML = ministryData.insights
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

// Render data table
function renderDataTable() {
  if (!ministryData.by_ministry) return;

  const sorted = Object.entries(ministryData.by_ministry).sort(
    (a, b) => b[1].total - a[1].total,
  );

  const table = `
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: var(--color-bg-alt); text-align: left;">
                    <th style="padding: var(--space-md); border: 1px solid var(--color-border);">Ministry</th>
                    <th style="padding: var(--space-md); border: 1px solid var(--color-border);">Total Sentences</th>
                    <th style="padding: var(--space-md); border: 1px solid var(--color-border);">Percentage</th>
                    <th style="padding: var(--space-md); border: 1px solid var(--color-border);">Peak Year</th>
                </tr>
            </thead>
            <tbody>
                ${sorted
                  .map(
                    ([ministry, data]) => `
                    <tr>
                        <td style="padding: var(--space-md); border: 1px solid var(--color-border);">${ministry}</td>
                        <td style="padding: var(--space-md); border: 1px solid var(--color-border);">${
                          data.total
                        }</td>
                        <td style="padding: var(--space-md); border: 1px solid var(--color-border);">${
                          data.percentage
                        }%</td>
                        <td style="padding: var(--space-md); border: 1px solid var(--color-border);">${
                          data.peak_year || "N/A"
                        }</td>
                    </tr>
                `,
                  )
                  .join("")}
            </tbody>
        </table>
    `;

  document.getElementById("dataTable").innerHTML = table;
}

// Download CSV
document.getElementById("downloadCSV")?.addEventListener("click", () => {
  if (!ministryData.by_ministry) return;

  const csv = [
    ["Ministry", "Total Sentences", "Percentage", "Peak Year"],
    ...Object.entries(ministryData.by_ministry)
      .sort((a, b) => b[1].total - a[1].total)
      .map(([ministry, data]) => [
        ministry,
        data.total,
        data.percentage,
        data.peak_year || "N/A",
      ]),
  ]
    .map((row) => row.join(","))
    .join("\n");

  downloadFile(csv, "ministries_data.csv", "text/csv");
});

// Utility: Get color for ministry (civic strength palette)
function getColorForMinistry(ministry) {
  const colors = {
    Defence: "#C8102E", // Vibrant Red
    Education: "#0C2340", // Deep Navy
    Health: "#2D6A4F", // Forest Green
    Housing: "#D4A72C", // Civic Gold
    Transport: "#3D7C8C", // Teal
    Economy: "#1A3A5C", // Steel Blue
    Finance: "#6B4E71", // Muted Purple
    "Social Services": "#B45A3C", // Terracotta
    Environment: "#2D6A4F", // Forest Green
    Technology: "#5C5C5C", // Charcoal
  };
  return colors[ministry] || "#9EA2A2";
}

// Utility: Get color by index (civic strength palette)
function getColorByIndex(index) {
  const colors = [
    "#0C2340", // Deep Navy
    "#C8102E", // Vibrant Red
    "#2D6A4F", // Forest Green
    "#D4A72C", // Civic Gold
    "#1A3A5C", // Steel Blue
    "#9EA2A2", // Slate Gray
    "#6B4E71", // Muted Purple
    "#B45A3C", // Terracotta
    "#3D7C8C", // Teal
    "#5C5C5C", // Charcoal
  ];
  return colors[index % colors.length];
}

// Utility: Download file
function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
