// ===================================
// GLOBAL REFERENCES PAGE
// Singapore Budget Speeches (1960-2025)
// ===================================

// Data cache
let overviewData = null;
let timeSeriesData = null;
let countryDetailsData = null;
let mapData = null;
let decadeShardCache = new Map(); // Cache for decade shards

// Region colors for consistent styling
const regionColors = {
  "East Asia": "#C8102E",
  "Southeast Asia": "#2D6A4F",
  "South Asia": "#B8941A",
  Oceania: "#3D7C8C",
  "Western Europe": "#0C2340",
  "Northern Europe": "#5C88A8",
  "Southern Europe": "#B45A3C",
  "Eastern Europe": "#6B4E71",
  "North America": "#1A3A5C",
  "Central America": "#7C9A3C",
  "South America": "#D4A03C",
  "Middle East": "#8B4513",
  "North Africa": "#CD853F",
  "Sub-Saharan Africa": "#556B2F",
};

// Initialize page
document.addEventListener("DOMContentLoaded", async () => {
  await loadAllData();
  renderPage();
});

// Load all required data files
async function loadAllData() {
  try {
    const [overview, timeSeries, details, map] = await Promise.all([
      fetch("data/summary/global_overview.json").then((r) => r.json()),
      fetch("data/summary/global_time_series.json").then((r) => r.json()),
      fetch("data/summary/global_country_details.json").then((r) => r.json()),
      fetch("data/summary/global_map_data.json").then((r) => r.json()),
    ]);

    overviewData = overview;
    timeSeriesData = timeSeries;
    countryDetailsData = details;
    mapData = map;

    console.log("Global data loaded:", {
      totalMentions: overview.total_mentions,
      countriesMentioned: overview.countries_mentioned,
    });
  } catch (error) {
    console.error("Failed to load global data:", error);
    document.getElementById("loading").innerHTML =
      '<p class="error">Failed to load data. Please refresh the page.</p>';
  }
}

// Render all page components
function renderPage() {
  document.getElementById("loading").style.display = "none";
  document.getElementById("content").style.display = "block";

  renderWorldMap();
  renderRegionCards();
  setupCountrySelectors();
  renderCountryTrends();
  populateRegionFilter();
  renderCountryList();
}

// ===================================
// WORLD MAP (Choropleth)
// ===================================
function renderWorldMap() {
  // Prepare data for choropleth
  const isoCodes = Object.keys(mapData);
  const values = isoCodes.map((iso) => mapData[iso].total);
  const countries = isoCodes.map((iso) => mapData[iso].country);
  const regions = isoCodes.map((iso) => mapData[iso].region);

  // Create hover text
  const hoverText = isoCodes.map((iso, i) => {
    const d = mapData[iso];
    return (
      `<b>${d.country}</b><br>` + `${d.total} mentions<br>` + `${d.region}`
    );
  });

  const trace = {
    type: "choropleth",
    locationmode: "ISO-3",
    locations: isoCodes,
    z: values,
    text: hoverText,
    hoverinfo: "text",
    colorscale: [
      [0, "#E8E6E3"],
      [0.1, "#D4E8DE"],
      [0.3, "#7CB9A0"],
      [0.5, "#4A9B73"],
      [0.7, "#2D6A4F"],
      [1, "#1B4332"],
    ],
    colorbar: {
      title: "Mentions",
      thickness: 15,
      len: 0.6,
      y: 0.5,
      tickfont: { size: 11 },
    },
    marker: {
      line: {
        color: "white",
        width: 0.5,
      },
    },
  };

  const layout = {
    geo: {
      showframe: false,
      showcoastlines: true,
      coastlinecolor: "#CCCCCC",
      projection: {
        type: "natural earth",
      },
      showland: true,
      landcolor: "#F5F5F5",
      showocean: true,
      oceancolor: "#E8F4F8",
      showcountries: true,
      countrycolor: "#DDDDDD",
      showlakes: false,
      resolution: 50,
    },
    margin: { t: 10, b: 10, l: 10, r: 10 },
    height: 450,
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ["lasso2d", "select2d"],
  };

  Plotly.newPlot("worldMap", [trace], layout, config);

  // Add click handler to scroll to country details
  document.getElementById("worldMap").on("plotly_click", (data) => {
    const iso = data.points[0].location;
    const countryName = mapData[iso]?.country;
    if (countryName && countryDetailsData[countryName]) {
      // Scroll to and expand that country
      const countryCard = document.querySelector(
        `[data-country="${countryName}"]`,
      );
      if (countryCard) {
        countryCard.scrollIntoView({ behavior: "smooth", block: "center" });
        // Expand if collapsed
        if (!countryCard.classList.contains("expanded")) {
          toggleCountryExpansion(countryName);
        }
      }
    }
  });
}

// ===================================
// REGION CARDS
// ===================================
function renderRegionCards() {
  const container = document.getElementById("regionCards");

  // Sort regions by total mentions
  const sortedRegions = Object.entries(overviewData.by_region)
    .sort((a, b) => b[1].total - a[1].total)
    .slice(0, 8); // Show top 8 regions

  container.innerHTML = sortedRegions
    .map(([region, data]) => {
      const color = regionColors[region] || "#666";
      const topCountries = Object.entries(data.countries)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([c, n]) => `${c} (${n})`)
        .join(", ");

      return `
      <div class="region-card" style="border-left: 4px solid ${color}">
        <h4>${region}</h4>
        <div class="region-total">${data.total.toLocaleString()} mentions</div>
        <div class="region-countries">${topCountries}</div>
      </div>
    `;
    })
    .join("");
}

// ===================================
// COUNTRY TRENDS CHART
// ===================================
function setupCountrySelectors() {
  const topCountries = Object.entries(overviewData.country_totals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20);

  const selectors = ["countrySelect1", "countrySelect2", "countrySelect3"];
  const defaults = ["United States", "China", "Malaysia"];

  selectors.forEach((id, index) => {
    const select = document.getElementById(id);
    select.innerHTML =
      '<option value="">-- Select Country --</option>' +
      topCountries
        .map(
          ([country]) =>
            `<option value="${country}" ${
              country === defaults[index] ? "selected" : ""
            }>${country}</option>`,
        )
        .join("");

    select.addEventListener("change", renderCountryTrends);
  });
}

function renderCountryTrends() {
  const selected = [
    document.getElementById("countrySelect1").value,
    document.getElementById("countrySelect2").value,
    document.getElementById("countrySelect3").value,
  ].filter(Boolean);

  if (selected.length === 0) {
    selected.push("United States", "China", "Malaysia");
  }

  const years = timeSeriesData.years;
  const traces = [];

  // Color palette for selected countries
  const colors = ["#C8102E", "#0C2340", "#2D6A4F", "#B8941A", "#6B4E71"];

  selected.forEach((country, i) => {
    const countryData = timeSeriesData.countries[country];
    if (countryData) {
      traces.push({
        x: years,
        y: countryData.yearly_counts,
        name: country,
        type: "scatter",
        mode: "lines+markers",
        line: {
          color: colors[i % colors.length],
          width: 2,
        },
        marker: {
          size: 5,
        },
        hovertemplate: `<b>${country}</b><br>%{x}: %{y} mentions<extra></extra>`,
      });
    }
  });

  // Add crisis year annotations
  const crisisYears = [
    { year: 1973, label: "Oil Crisis" },
    { year: 1985, label: "Recession" },
    { year: 1997, label: "Asian Crisis" },
    { year: 2008, label: "Global Crisis" },
    { year: 2020, label: "COVID-19" },
  ];

  const annotations = crisisYears.map((crisis) => ({
    x: crisis.year,
    y: 1,
    yref: "paper",
    text: crisis.label,
    showarrow: true,
    arrowhead: 0,
    ax: 0,
    ay: -25,
    font: { size: 9, color: "#888" },
  }));

  const layout = {
    showlegend: true,
    legend: {
      orientation: "h",
      y: -0.15,
      x: 0.5,
      xanchor: "center",
    },
    xaxis: {
      title: "Year",
      tickmode: "linear",
      dtick: 10,
      gridcolor: "#E5E5E5",
    },
    yaxis: {
      title: "Number of Mentions",
      gridcolor: "#E5E5E5",
    },
    margin: { t: 30, b: 80, l: 60, r: 20 },
    height: 400,
    plot_bgcolor: "white",
    paper_bgcolor: "white",
    annotations: annotations,
  };

  Plotly.newPlot("countryTrendsChart", traces, layout, { responsive: true });
}

// ===================================
// COUNTRY LIST WITH EXPANDABLE QUOTES
// ===================================
function populateRegionFilter() {
  const select = document.getElementById("regionFilter");
  const regions = [
    ...new Set(Object.values(countryDetailsData).map((c) => c.region)),
  ].sort();

  select.innerHTML =
    '<option value="">All Regions</option>' +
    regions.map((r) => `<option value="${r}">${r}</option>`).join("");

  select.addEventListener("change", renderCountryList);
  document
    .getElementById("sortBy")
    .addEventListener("change", renderCountryList);
}

function renderCountryList() {
  const container = document.getElementById("countryList");
  const regionFilter = document.getElementById("regionFilter").value;
  const sortBy = document.getElementById("sortBy").value;

  // Filter and sort countries
  let countries = Object.entries(countryDetailsData).map(([name, data]) => ({
    name,
    ...data,
  }));

  if (regionFilter) {
    countries = countries.filter((c) => c.region === regionFilter);
  }

  switch (sortBy) {
    case "mentions":
      countries.sort((a, b) => b.total_mentions - a.total_mentions);
      break;
    case "name":
      countries.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case "recent":
      countries.sort((a, b) => {
        const aYears = Object.keys(a.by_year).map(Number);
        const bYears = Object.keys(b.by_year).map(Number);
        return Math.max(...bYears) - Math.max(...aYears);
      });
      break;
  }

  container.innerHTML = countries
    .map((country) => {
      const years = Object.keys(country.by_year).sort();
      const yearRange =
        years.length > 0
          ? `${years[0]}–${years[years.length - 1]}`
          : "No mentions";
      const color = regionColors[country.region] || "#666";

      return `
      <div class="country-card" data-country="${country.name}">
        <div class="country-header" onclick="toggleCountryExpansion('${
          country.name
        }')">
          <div class="country-info">
            <span class="country-name">${country.name}</span>
            <span class="country-region" style="color: ${color}">${
              country.region
            }</span>
          </div>
          <div class="country-stats">
            <span class="mention-count">${
              country.total_mentions
            } mentions</span>
            <span class="year-range">${yearRange}</span>
            <span class="expand-icon">▼</span>
          </div>
        </div>
        <div class="country-details" id="details-${country.name.replace(
          /\s+/g,
          "-",
        )}">
          ${renderCountryQuotes(country)}
        </div>
      </div>
    `;
    })
    .join("");
}

function renderCountryQuotes(country) {
  const yearGroups = Object.entries(country.by_year)
    .sort((a, b) => Number(b[0]) - Number(a[0])) // Most recent first
    .slice(0, 10); // Limit to 10 years for performance

  if (yearGroups.length === 0) {
    return "<p>No quotes available.</p>";
  }

  let quoteIndex = 0;
  return yearGroups
    .map(([year, quotes]) => {
      const quotesHtml = quotes
        .slice(0, 3) // Show max 3 quotes per year
        .map((q) => {
          const currentIndex = quoteIndex++;
          const highlightedText = highlightTerms(q.text, q.terms);
          const quoteId = `quote-${country.name.replace(
            /\s+/g,
            "-",
          )}-${currentIndex}`;
          return `
          <div class="quote-item" data-year="${year}" data-text="${encodeURIComponent(
            q.text,
          )}">
            <p class="quote-text">${highlightedText}</p>
            <div class="quote-actions">
              ${
                q.section
                  ? `<span class="quote-section">${q.section}</span>`
                  : ""
              }
              <button class="context-toggle" onclick="toggleQuoteContext('${quoteId}', '${
                country.name
              }', ${year}, '${encodeURIComponent(
                q.text,
              )}')" title="Show surrounding context">
                ▼ Context
              </button>
            </div>
            <div class="quote-context" id="${quoteId}" style="display: none;">
              <div class="context-loading">Loading context...</div>
            </div>
          </div>
        `;
        })
        .join("");

      const moreCount = quotes.length - 3;
      const moreIndicator =
        moreCount > 0
          ? `<p class="more-quotes">+ ${moreCount} more quote${
              moreCount > 1 ? "s" : ""
            } in ${year}</p>`
          : "";

      return `
      <div class="year-group">
        <h5 class="year-label">${year}</h5>
        ${quotesHtml}
        ${moreIndicator}
      </div>
    `;
    })
    .join("");
}

function highlightTerms(text, terms) {
  let highlighted = text;
  terms.forEach((term) => {
    const regex = new RegExp(`(${escapeRegex(term)})`, "gi");
    highlighted = highlighted.replace(regex, "<mark>$1</mark>");
  });
  return highlighted;
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Toggle country expansion
function toggleCountryExpansion(countryName) {
  const card = document.querySelector(`[data-country="${countryName}"]`);
  const details = document.getElementById(
    `details-${countryName.replace(/\s+/g, "-")}`,
  );
  const icon = card.querySelector(".expand-icon");

  if (card.classList.contains("expanded")) {
    card.classList.remove("expanded");
    details.style.display = "none";
    icon.textContent = "▼";
  } else {
    card.classList.add("expanded");
    details.style.display = "block";
    icon.textContent = "▲";
  }
}

// Toggle quote context expansion
async function toggleQuoteContext(quoteId, countryName, year, encodedText) {
  const contextDiv = document.getElementById(quoteId);
  const button =
    contextDiv.previousElementSibling.querySelector(".context-toggle");
  const text = decodeURIComponent(encodedText);

  if (contextDiv.style.display === "none") {
    contextDiv.style.display = "block";
    button.textContent = "▲ Hide";
    button.classList.add("active");

    // Load context if not already loaded
    if (contextDiv.querySelector(".context-loading")) {
      await loadQuoteContext(quoteId, year, text);
    }
  } else {
    contextDiv.style.display = "none";
    button.textContent = "▼ Context";
    button.classList.remove("active");
  }
}

// Load surrounding context for a quote
async function loadQuoteContext(quoteId, year, text) {
  const contextDiv = document.getElementById(quoteId);

  // Determine decade from year
  const decade = `${Math.floor(year / 10) * 10}s`;
  const shardPath = `data/search-index/decades/${decade}.json`;

  // Load decade shard if not cached
  if (!decadeShardCache.has(decade)) {
    try {
      const response = await fetch(shardPath);
      if (!response.ok) throw new Error("Failed to fetch");
      const data = await response.json();
      decadeShardCache.set(decade, data);
    } catch (error) {
      console.error("Failed to load decade shard:", error);
      contextDiv.innerHTML = "<em>Context not available</em>";
      return;
    }
  }

  const shard = decadeShardCache.get(decade);
  if (!shard || !shard.sentences) {
    contextDiv.innerHTML = "<em>Context not available</em>";
    return;
  }

  // Find sentences from the same year
  const yearSentences = shard.sentences.filter((s) => s.year === year);

  // Find the index of the current sentence by matching text
  const currentIdx = yearSentences.findIndex(
    (s) => s.text === text || s.text.includes(text) || text.includes(s.text),
  );

  if (currentIdx === -1) {
    contextDiv.innerHTML = "<em>Context not available for this quote</em>";
    return;
  }

  // Get surrounding sentences (3 before, 3 after)
  const contextRange = 3;
  const startIdx = Math.max(0, currentIdx - contextRange);
  const endIdx = Math.min(yearSentences.length - 1, currentIdx + contextRange);

  const contextSentences = yearSentences.slice(startIdx, endIdx + 1);

  // Build context HTML
  const contextHtml = contextSentences
    .map((sentence, i) => {
      const actualIdx = startIdx + i;
      const isCurrent = actualIdx === currentIdx;

      return `<p class="${
        isCurrent ? "context-current" : "context-surrounding"
      }">${sentence.text}</p>`;
    })
    .join("");

  contextDiv.innerHTML = `<div class="context-content">${contextHtml}</div>`;
}

// Expose functions globally
window.toggleCountryExpansion = toggleCountryExpansion;
window.toggleQuoteContext = toggleQuoteContext;
