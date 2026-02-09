# Website Strategy: Singapore Budget Speeches (1960-2025)

**Project Goal:** Create a reader-centric interactive website that tells the story of Singapore's policy evolution through 65 years of budget speeches, backed by rigorous statistical analysis.

**Target Audience:** Policy researchers, students, journalists, curious citizens, and data enthusiasts.

---

## Table of Contents
1. [Core Philosophy](#core-philosophy)
2. [Three Reading Paths](#three-reading-paths)
3. [Site Architecture](#site-architecture)
4. [Page-by-Page Specifications](#page-by-page-specifications)
5. [Statistical Integration](#statistical-integration)
6. [Design System](#design-system)
7. [Technical Implementation](#technical-implementation)
8. [GitHub Pages Deployment](#github-pages-deployment)
9. [Data Export Pipeline](#data-export-pipeline)
10. [Development Checklist](#development-checklist)

---

## Core Philosophy

### Reader-Centric Design Principles

1. **Progressive Disclosure**: Start with narrative, expand to details
   - Casual readers get the story (5 mins)
   - Curious analysts explore patterns (15 mins)
   - Researchers access full data (30+ mins)

2. **Statistics as Evidence, Not Obstacle**
   - Every insight backed by real sentence examples
   - Data hidden in collapsible panels, shown on demand
   - Numbers contextualized with historical events

3. **Multiple Entry Points**
   - Home → Search → Ministries → Ministers → Language → About
   - Quick questions → Direct answers
   - Topic buttons → Relevant sections

4. **Narrative Arc**
   - Singapore's journey: Survival → Growth → Inclusivity → Sustainability
   - 7 Finance Ministers, each with distinct voice
   - 4 major crises, revealing policy responses

---

## Three Reading Paths

### Path 1: The Storyteller (5 minutes)
**Target:** Casual reader wanting highlights

**Experience:**
- Landing page with compelling intro: "65 Years of Policy in 40,000 Sentences"
- 4 stat cards with hover tooltips
- 3 entry cards: "Start the Story" | "Explore by Theme" | "Dive into Data"
- Guided narrative tour (optional auto-play through 10 key moments)

**Journey:**
```
Index → Featured Insight → Minister Profile → Crisis Response → Key Quote → Done
```

---

### Path 2: The Explorer (15 minutes)
**Target:** Analyst wanting to understand patterns

**Experience:**
- Interactive visualizations (Plotly charts)
- Ministry trends over time (stacked area, heatmaps)
- Minister comparison (focus areas, linguistic styles)
- Crisis response patterns (before/during/after)
- Clickable data points revealing sample sentences

**Journey:**
```
Index → Ministries (see trends) → Click 2015 → See Heng's social policy focus
→ Ministers page → Compare Heng vs Tharman → Language page → See complexity decline
```

---

### Path 3: The Researcher (30+ minutes)
**Target:** Academic/policy analyst needing full data

**Experience:**
- All visualizations + expandable statistical tables
- Full CSV downloads (9 files)
- Methodology documentation
- Search with advanced filters
- Representative sentences by era/minister/ministry
- Direct GitHub repository access

**Journey:**
```
Index → Search for "healthcare subsidies" → Filter by Tharman → Read 50 results
→ Ministers page → Expand statistical breakdown → Download ministry_by_minister.csv
→ About page → Read methodology → Clone GitHub repo
```

---

## Site Architecture

### 6-Page Structure

```
singapore-budget-speeches/
└── docs/
  ├── index.html                # Homepage with 3 entry paths
  ├── search.html               # Search experience with filters
  ├── ministries.html           # Ministry trends & decade heatmap
  ├── ministers.html            # Finance Minister comparison
  ├── language.html             # Linguistic evolution analysis
  ├── about.html                # Methodology & credits
  │
  ├── assets/
  │   ├── app.[hash].js         # Page bootstrap, shared routing
  │   ├── vendor.[hash].js      # Plotly + utility bundle
  │   └── style.[hash].css      # Tokens + layout system
  │
  └── data/
    ├── summary/
    │   ├── ministries.json   # <=200 KB initial payloads
    │   ├── ministers.json
    │   ├── language.json
    │   └── crises.json
    │
    ├── detailed/
    │   ├── ministries-1960s.json   # Lazy-loaded time slices
    │   ├── ministries-1970s.json
    │   ├── ministers-focus.json
    │   └── language-trends.json
    │
    └── search-index/
      ├── overview.json     # Default scoped index
      ├── decades/
      │   ├── 1960s.json
      │   ├── 1970s.json
      │   └── ...
      └── topics/
        ├── social.json
        ├── fiscal.json
        └── ...
```

**Bundled Assets:** A single Vite build fingerprints the js/css into docs/assets/ so Plotly and helpers load once per session across every page. Source modules stay human-readable in src/ (search.js, ministries.js, ministers.js, language.js).

**Deployment Note:** GitHub Pages serves the bundled assets above, keeping all six pages routable so every chart, narrative, and dataset remains visible.

**Progressive Loading:** Each page boots with a <=200 KB summary payload and surfaces a "Load full dataset" control that fetches extra JSON shards from docs/data/ on demand. Every insight documented below stays reachable once a visitor opts in.

**Search Archives:** Search opens with docs/data/search-index/overview.json for instant answers. Choosing "Expand to 40,000 sentences" streams decade/topic shards so power users can still roam the entire corpus in-browser without penalising casual readers.

---

## Page-by-Page Specifications

### 1. Index (Homepage)

**Purpose:** Set narrative stage, guide users to relevant content

**Sections:**

#### A. Hero Section
```
"65 Years of Policy in 40,000 Sentences"
Singapore's Budget Speeches (1960-2025)

From post-independence survival to sustainability leadership,
seven Finance Ministers shaped our nation through their words.

[Start Exploring →]
```

#### B. Key Statistics (4 Cards with Context)
```
┌─────────────────────────────────────────┐
│ 40,123 sentences                        │
│ Hover: "Enough to fill 15 novels"      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 66 speeches                             │
│ Hover: "One every year since 1960"     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 7 Finance Ministers                     │
│ Hover: "From Goh Keng Swee to Lawrence  │
│         Wong"                           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 15 Policy Areas                         │
│ Hover: "Defence, Education, Health...   │
│         see how priorities shifted"     │
└─────────────────────────────────────────┘
```

#### C. Three Entry Paths (Visual Cards)

**Card 1: "Start the Story" 🎬**
- Guided narrative tour through 10 key moments
- Auto-play option (like a slideshow)
- Timeline: 1960s nation-building → 2020s sustainability
- CTA: "Begin the Journey"

**Card 2: "Explore by Theme" 🔍**
- Interactive visualizations
- Ministry trends, minister styles, crisis responses
- Each chart clickable for deeper insights
- CTA: "See the Patterns"

**Card 3: "Dive into Data" 📊**
- Full statistical breakdowns
- Downloadable CSV files
- Methodology documentation
- CTA: "Access the Numbers"

#### D. Quick Questions (Jump-to Buttons)
```
"What are you curious about?"

[How did speeches change during crises?] → Crisis analysis
[Which minister focused on social policy?] → Minister comparison
[When did sustainability become priority?] → Ministry trends
[How readable are these speeches?] → Language analysis
```

#### E. Footer Navigation
```
Explore More: [Search] [Ministries] [Ministers] [Language] [About]
Data Source: Singapore Parliament Hansard (1960-2025)
```

---

### 2. Search Page

**Purpose:** Find specific topics, quotes, policy discussions

**Sections:**

#### A. Guided Search Suggestions (Before Search Box)
```
"What are you researching?"

[📈 Economic Policy] → Suggests: "GDP, restructuring, productivity"
[🏥 Healthcare] → Suggests: "Medisave, hospital, healthcare subsidies"
[🏠 Housing] → Suggests: "HDB, flats, resale, BTO"
[💼 Jobs & Skills] → Suggests: "CPF, employment, training, Workfare"
[🌱 Environment] → Suggests: "carbon, climate, sustainability, green"
```

#### B. Search Interface
```
┌────────────────────────────────────────────────────────┐
│ Search 40,000 sentences (instant overview)...   [🔍]   │
└────────────────────────────────────────────────────────┘

Scope:
[●] Overview (<=60 results, ~150KB)   [○] Full Archive (requires download)
⬇️ Button: "Expand to full archive (~3MB)"

Filters:
[Year/Decade ▼] [Minister ▼] [Ministry Topic ▼]
```

#### C. Search Results (Context-Rich Cards)
```
┌─────────────────────────────────────────────────────────┐
│ [1985, Goh Keng Swee, Finance]                          │
│ "We will restructure the economy by reducing costs..."  │
│                                                          │
│ 📊 Context:                                             │
│ • Overview scope: 60 most relevant sentences           │
│ • Expand archive to unlock +3,000 crisis-era quotes    │
│ • Goh's speeches averaged 20.6 words/sentence          │
│                                                          │
│ 🔗 Related: [See other crisis responses] [View Goh's   │
│             profile]                                    │
└─────────────────────────────────────────────────────────┘
```

#### D. Statistics Sidebar (Collapsible)
```
▼ Search Statistics

Total matches: 147 sentences (Overview scope)

By Decade:
1960s: 12 (8%)
1970s: 18 (12%)
...

By Minister:
Goh Keng Swee: 45 (31%)
Tharman: 28 (19%)
...

By Ministry:
Finance: 62 (42%)
Trade & Industry: 35 (24%)
...

Note: Counts recalculate after "Expand to full archive" downloads decade/topic shards.
```

---

### 3. Ministries Page

**Purpose:** Show how Singapore's policy priorities evolved across 15 ministries

**Sections:**

#### A. Narrative Opening
```
"Singapore's Shifting Priorities"

In 1960, Defence dominated 22% of Goh Keng Swee's speech.
By 2025, it's 5%. What changed? Everything.

Follow how 15 policy areas rose and fell across 65 years.
```

#### B. Interactive Stacked Area Chart
- Ministry distribution 1960-2025 (Plotly)
- Hover: "Finance 1985: 18.3% of speech"
- Click any area → Expands to show:
  - Top 5 sentences from that ministry-year
  - Historical context (e.g., "1985 Recession year")
  - Link to minister profile

**Visual:**
```
100% ┌─────────────────────────────────────────┐
     │░░░░ General                             │
     │████ Defence                             │
75%  │████ Finance                             │
     │▓▓▓▓ Trade & Industry                   │
     │▒▒▒▒ Education                           │
50%  │░░░░ Manpower                            │
     │░░░░ Health                              │
     │░░░░ Transport                           │
25%  │░░░░ Other ministries...                 │
     │                                         │
0%   └─────────────────────────────────────────┘
     1960  1970  1980  1990  2000  2010  2020
```

#### C. Four Eras of Development (Decade Heatmap)
```
┌────────────────────────────────────────────────────────┐
│                 1960s 1970s 1980s 1990s 2000s 2010s 2020s│
│ Defence         19.8  18.2  16.4  14.1  10.2   8.1   5.3 │
│ Finance         15.2  14.8  17.4  15.9  13.2  12.4  11.8 │
│ Education        8.1   7.9   6.8   6.2   7.4   8.9   7.2 │
│ Manpower         4.2   4.8   5.1   6.3   8.2   9.8   8.4 │
│ ...                                                       │
└────────────────────────────────────────────────────────┘

Era Labels:
1960s-70s: Survival & Security
1980s-90s: Economic Transformation
2000s-10s: Inclusive Growth
2020s: Sustainable Future
```

#### D. Expandable Statistics Panel
```
▼ See Full Statistical Breakdown

[Table: ministry_topic_statistics.csv]
Ministry | Total Sentences | % | Peak Year | Years Mentioned
Defence  | 7,509          | 18.9% | 1961     | 66
Finance  | 6,010          | 15.1% | 2002     | 66
...

[Download CSV]
```

**Data Loading:** The stacked area, heatmap, and table boot from summary/ministries.json (<200KB). Selecting "See Full Statistical Breakdown" pulls the matching detailed/ministries-XXXX.json shard before rendering the expanded view.

#### E. Rising & Falling Topics (Diverging Bar Chart)
```
Emerging Topics:                     Declining Topics:
Sustainability & Environment ████████ │ ████████ Defence
Manpower                    ████      │ ████ Foreign Affairs
Health                      ███       │
```

**Click any bar** → Shows 3 representative sentences

---

### 4. Ministers Page

**Purpose:** Compare 7 Finance Ministers' policy focus and linguistic styles

**Sections:**

#### A. Narrative Opening
```
"Seven Leaders, Seven Styles"

From Goh Keng Swee's crisp directives (20.6 words/sentence)
to Heng Swee Keat's inclusive language (18.0 words/sentence),
each minister brought their own voice to the budget.
```

#### B. Minister Timeline (Interactive Horizontal)
```
[1959────────1984] Goh Keng Swee (26 speeches)
         [1983-85] Tony Tan (3 speeches)
              [1985──────────2001] Richard Hu (17 speeches)
                      [2001──07] Lee HL (7 speeches)
                            [2007────────2015] Tharman (9 speeches)
                                    [2015──21] Heng (7 speeches)
                                          [2021─25] Wong (5 speeches)
```

**Click any minister** → Expands to Minister Profile Card:

#### C. Minister Profile Card (Example: Tharman)
```
┌─────────────────────────────────────────────────────────┐
│ Tharman Shanmugaratnam (2007-2015)                      │
│ 9 speeches | 15,300 words avg | 800 sentences avg      │
│                                                          │
│ "The Social Reformer"                                   │
│ Highest focus on: Manpower (9.2%), Health (3.1%),      │
│                   Social & Family Development (2.8%)    │
│                                                          │
│ Key Innovation: Introduced Workfare during 2008 crisis  │
│                                                          │
│ 📈 His Era:                                             │
│ • Global Financial Crisis (2008-2009)                   │
│ • Healthcare reforms (Medishield Life)                  │
│ • Pioneer Generation Package (2014)                     │
│                                                          │
│ Reading Complexity:                                     │
│ • 19.2 words/sentence (moderate)                        │
│ • Flesch Score: 54.8 (standard difficulty)             │
│                                                          │
│ ▼ See 3 Most Representative Quotes                      │
│ ▼ See Full Statistical Profile                          │
└─────────────────────────────────────────────────────────┘
```

#### D. Minister Comparison Heatmap
```
                    Defence Finance Education Manpower Health ...
Goh Keng Swee         25.2    16.8      5.4      4.2    1.8
Tony Tan              23.1    18.2      5.1      4.8    1.9
Richard Hu            18.4    19.3      5.6      5.2    2.1
Lee Hsien Loong       14.2    15.7      7.8      6.4    2.4
Tharman               11.8    14.3      6.9      9.2    3.1
Heng Swee Keat         9.4    12.8      7.2      9.8    2.9
Lawrence Wong          8.1    11.9      6.8      8.4    2.8
```

**Data Loading:** Timeline and heatmap render instantly from summary/ministers.json. The first profile expansion fetches detailed/ministers-focus.json and keeps it cached for comparisons, quote drawers, and CSV downloads.

**Hover each cell** → Shows:
- Exact percentage
- Sample sentence
- Comparison to other ministers

#### E. Crisis Responses
```
How each minister handled crises during their tenure:

1985 Recession → Goh Keng Swee
• Defence: -3.2pp
• Finance: +4.1pp
• Trade & Industry: +2.8pp

1997 Asian Crisis → Richard Hu
• Finance: +5.3pp
• Social & Family: +0.8pp

2008 Global Crisis → Tharman Shanmugaratnam
• Manpower: +2.7pp
• Social & Family: +1.4pp
• Health: +1.1pp

2020 COVID-19 → Heng Swee Keat
• Health: +1.9pp
• Social & Family: +1.1pp
• Sustainability: +0.8pp
```

#### F. Expandable Statistics
```
▼ Full Minister Statistics

[Table: minister_speech_statistics.csv]
Minister | Avg Words | Avg Sentences | Words/Sentence
Tharman  | 15,300   | 800.9        | 19.17
...

[Table: ministry_by_minister.csv - Full matrix]

[Download All Minister Data]
```

---

### 5. Language Page

**Purpose:** Show how budget speech language evolved over 65 years

**Sections:**

#### A. Narrative Opening
```
"How Budget Speeches Changed Their Voice"

1960: "We shall build factories and create jobs."
→ 22.4 words/sentence | Flesch 58.1 (standard)

2025: "Through SkillsFuture and progressive wage policies,
      we empower every Singaporean to thrive."
→ 18.1 words/sentence | Flesch 52.3 (slightly harder)

What changed? Not just complexity—entire vocabulary shifted.
```

#### B. Five Interactive Charts (Plotly)

**Chart 1: Readability Trends**
- Line chart: Flesch Reading Ease Score (1960-2025)
- Higher = easier to read
- Annotated events: "1985 Recession", "2008 Crisis"

**Chart 2: Sentence Length Over Time**
- Line chart: Average words per sentence by year
- Trend: Declining from 21+ to 18 words/sentence

**Chart 3: Vocabulary Complexity (Dual Axis)**
- Average word length (syllables)
- Vocabulary diversity (unique words per 100)

**Chart 4: Minister Comparison (Grouped Bars)**
- Readability by minister
- Sentence length by minister
- Shows Goh = most complex, Heng = most accessible

**Chart 5: Formality Evolution**
- Formality score over time
- 1960s: Formal, directive ("shall", "must")
- 2020s: Inclusive, aspirational ("together", "empower")

**Data Loading:** Charts 1-5 initialise from summary/language.json. Expanding any era card or downloading CSV triggers a single fetch of detailed/language-trends.json which stays cached for subsequent interactions.

#### C. Four-Era Timeline
```
1960s-1970s: Plain Language Era
"We shall expand industries and create employment."
• Avg: 21.2 words/sentence
• Flesch: 59.4 (standard)
• Style: Directive, economical

1980s-1990s: Technical Sophistication
"The restructuring of our economy necessitates comprehensive
manpower development strategies."
• Avg: 20.8 words/sentence
• Flesch: 56.2 (fairly difficult)
• Style: Bureaucratic, policy-heavy

2000s-2010s: Inclusive Complexity
"We will enhance support for lower-income families through
Workfare and healthcare subsidies."
• Avg: 19.4 words/sentence
• Flesch: 54.1 (fairly difficult)
• Style: Empathetic, multi-clause

2020s: Data-Driven Narratives
"Building on our Green Plan 2030, we will accelerate our
net-zero transition."
• Avg: 18.1 words/sentence
• Flesch: 52.8 (fairly difficult)
• Style: Forward-looking, sustainability-focused
```

#### D. Words That Define Each Era
```
▼ Keyword Evolution by Decade

1960s-1970s: "defence, economic, development, industrial"
1980s-1990s: "restructuring, services, productivity, global"
2000s-2010s: "inclusive, healthcare, upgrading, innovation"
2020s: "sustainability, digital, resilience, climate"
```

#### E. Expandable Statistics
```
▼ See Full Linguistic Data

[Table: yearly_speech_statistics.csv]
Year | Words/Sentence | Flesch Score | Complexity | Minister
1960 | 21.0          | 59.6        | Moderate  | Goh
1961 | 20.8          | 59.9        | Moderate  | Goh
...

[Chart: Readability Distribution by Minister]
[Download Linguistic Analysis CSV]
```

---

### 6. About Page

**Purpose:** Methodology transparency, data sources, credits

**Sections:**

#### A. How to Use This Site
```
Three Ways to Explore:

1. The Storyteller (5 min): Get the highlights
   → Start at homepage → "Start the Story" card

2. The Explorer (15 min): Understand patterns
   → Interactive charts → Click data points

3. The Researcher (30+ min): Deep dive into data
   → Full statistics → Download CSVs
```

#### B. The Data Behind the Story
```
Dataset Overview:
• 40,123 sentences analyzed
• 66 budget speeches (1960-2025)
• 7 Finance Ministers
• 15 ministry classifications
• 7 linguistic metrics
• 4 crisis periods examined

Data Source:
Singapore Parliament Official Reports (Hansard)
https://sprs.parl.gov.sg/

Processing Pipeline:
Raw PDF → Markdown → Sentence Parsing → Classification → Analysis
```

#### C. Methodology

**1. Ministry Topic Classification**
```
Approach: Weighted keyword matching

Each ministry has 10-30 keywords (e.g., Defence: "defence",
"military", "saf", "national service")

Multi-word keywords get higher weights:
• "national service" = 2 points
• "defence" = 1 point

Sentence assigned to ministry with highest score.
Sentences with no clear match = "general"

Accuracy: 82.7% of sentences classified to specific ministries
```

**2. Linguistic Analysis**
```
Metrics Calculated:
• Flesch Reading Ease Score
  Formula: 206.835 - 1.015(words/sentence) - 84.6(syllables/word)

• Average sentence length (words)
• Average word complexity (syllables)
• Vocabulary diversity (unique words per 100 words)
• Formality score (frequency of formal markers)
```

**3. Crisis Analysis**
```
4 Major Crises Examined:
• 1985 Recession
• 1997 Asian Financial Crisis
• 2008 Global Financial Crisis
• 2020 COVID-19 Pandemic

Method: Compare ministry distribution in 3-year windows:
• Before (3 years prior)
• During (crisis period)
• After (3 years post)
```

#### D. Explore the Code & Data
```
Full Analysis on GitHub:
https://github.com/parleh-mate/singapore-budget-speeches

Repository Contents:
• Jupyter notebooks (analysis/)
• Python extraction scripts (extractor/)
• Processed data (output_processor/)
• Raw speeches (output_markdown/)

Download Data:
[ministry_by_year.csv]
[ministry_by_minister.csv]
[ministry_by_decade.csv]
[ministry_topic_statistics.csv]
[yearly_speech_statistics.csv]
[minister_speech_statistics.csv]
[linguistic_analysis.csv]
[crisis_analysis.csv]
[search-index/overview.json (~150KB)]
[search-index/decades/1960s.json]
[search-index/decades/1970s.json]
[search-index/topics/social_support.json]
[search-index/topics/fiscal_policy.json]
[Full archive shards in docs/data/search-index/]
```

#### E. Credits & Acknowledgments
```
Analysis & Design: Jeremy Chia

Data Source: Singapore Parliament
Hansard archives (1960-2025)

Libraries Used:
• Python: pandas, matplotlib, seaborn, scikit-learn
• JavaScript: Plotly.js (charts)
• CSS: Minimalist design system

License: MIT (code) | Data from public government sources
```

---

## Statistical Integration

### Progressive Disclosure Strategy

**Level 1: Always Visible (Storyteller)**
- Key insights in plain language
- 1-2 sentence summaries
- Visual charts without numbers

**Level 2: Expandable (Explorer)**
- Click "📊 See Statistics" → Panel slides down
- Summary tables (top 5-10 rows)
- Interactive chart tooltips

**Level 3: Downloadable (Researcher)**
- Full CSV files
- Complete statistical tables
- GitHub repository link

### Example: Ministries Page

```html
<!-- Level 1: Narrative -->
<div class="insight">
  Defence dominated early speeches (22% in 1960) but declined
  to 5% by 2025 as Singapore matured from survival to prosperity.
</div>

<!-- Level 2: Expandable -->
<details class="stats-panel">
  <summary>📊 See Defence Statistics</summary>
  <table>
    <tr><td>1960s avg:</td><td>19.8%</td></tr>
    <tr><td>2020s avg:</td><td>5.3%</td></tr>
    <tr><td>Peak year:</td><td>1961 (200 sentences)</td></tr>
  </table>

  <h4>Sample Sentences from 1961:</h4>
  <blockquote>
    "We must build a credible defence force to ensure our
    survival as an independent nation."
  </blockquote>
</details>

<!-- Level 3: Download -->
<a href="data/ministry_by_year.csv" download>
  Download Full Dataset
</a>
```

---

## Design System

### Minimalist Aesthetic

**Philosophy:** Let the data story shine, not the design.

### Color Palette

```css
:root {
  /* Primary Colors */
  --primary: #2E86AB;        /* Singapore blue */
  --secondary: #A23B72;      /* Accent purple */
  --success: #6A994E;        /* Green for positive */
  --warning: #F77F00;        /* Orange for attention */
  --danger: #E63946;         /* Red for decline */

  /* Neutral Palette */
  --text: #1a1a1a;           /* Near-black text */
  --text-muted: #666;        /* Secondary text */
  --bg: #ffffff;             /* White background */
  --bg-gray: #f8f9fa;        /* Light gray panels */
  --border: #e0e0e0;         /* Subtle borders */

  /* Ministry Colors (from notebook) */
  --ministry-defence: #5F0F40;
  --ministry-finance: #2E86AB;
  --ministry-education: #C73E1D;
  --ministry-manpower: #F18F01;
  --ministry-health: #6A994E;
  /* ... all 15 ministries */
}
```

### Typography

```css
:root {
  /* Font Stack */
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono: "SF Mono", Monaco, "Cascadia Code", Consolas,
               "Courier New", monospace;

  /* Type Scale */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}

body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--text);
}

h1 { font-size: var(--text-4xl); line-height: var(--leading-tight); }
h2 { font-size: var(--text-3xl); line-height: var(--leading-tight); }
h3 { font-size: var(--text-2xl); line-height: var(--leading-normal); }
```

### Spacing System

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

### Component Styles

**1. Stat Card**
```css
.stat-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: var(--space-6);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.stat-number {
  font-size: var(--text-4xl);
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin-top: var(--space-2);
}
```

**2. Expandable Statistics Panel**
```css
.stats-panel {
  margin: var(--space-8) 0;
  padding: var(--space-6);
  background: var(--bg-gray);
  border-left: 4px solid var(--primary);
  border-radius: 4px;
}

.stats-panel summary {
  cursor: pointer;
  font-weight: 600;
  user-select: none;
}

.stats-panel[open] {
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**3. Sample Sentence Card**
```css
.sample-sentence {
  border-left: 3px solid var(--ministry-color);
  padding: var(--space-4) var(--space-6);
  margin: var(--space-3) 0;
  background: var(--bg-gray);
  font-style: italic;
  border-radius: 0 4px 4px 0;
}

.sentence-meta {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin-top: var(--space-2);
  font-style: normal;
}
```

**4. Ministry Badge**
```css
.ministry-badge {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  border-radius: 12px;
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.ministry-badge.defence {
  background: rgba(95, 15, 64, 0.1);
  color: var(--ministry-defence);
}

.ministry-badge.finance {
  background: rgba(46, 134, 171, 0.1);
  color: var(--ministry-finance);
}
/* ... etc for all 15 ministries */
```

### Responsive Breakpoints

```css
/* Mobile-first approach */

/* Small devices (phones, 640px and down) */
@media (max-width: 640px) {
  .stat-grid { grid-template-columns: 1fr; }
  .chart-container { height: 300px; }
}

/* Medium devices (tablets, 641px-1024px) */
@media (min-width: 641px) {
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  .chart-container { height: 400px; }
}

/* Large devices (desktops, 1025px and up) */
@media (min-width: 1025px) {
  .stat-grid { grid-template-columns: repeat(4, 1fr); }
  .chart-container { height: 500px; }
}
```

---

## Technical Implementation

### Technology Stack

**Frontend:**
- HTML5 (semantic markup)
- CSS3 (custom properties, grid, flexbox)
- Vanilla JavaScript (ES6+)
- Plotly.js (interactive charts)

**No Frameworks:** Keep it simple, fast, and maintainable.

**Why No React/Vue/etc?**
- Static data (no real-time updates)
- Better performance (no bundle overhead)
- Easier for future contributors
- GitHub Pages compatibility

---

### JavaScript Architecture

**1. Search Engine (search.js)**

```javascript
// Progressive search loading
let overviewData = [];
const shardCache = new Map();

async function ensureOverviewLoaded() {
  if (overviewData.length) return overviewData;
  const response = await fetch('data/search-index/overview.json');
  overviewData = await response.json();
  console.log(`Loaded ${overviewData.length} overview sentences`);
  return overviewData;
}

async function ensureShardLoaded(type, key) {
  const cacheKey = `${type}:${key}`;
  if (shardCache.has(cacheKey)) {
    return shardCache.get(cacheKey);
  }

  const response = await fetch(`data/search-index/${type}/${key}.json`);
  const data = await response.json();
  shardCache.set(cacheKey, data);
  console.log(`Loaded ${data.length} sentences for ${cacheKey}`);
  return data;
}

async function getSearchDataset(scope) {
  if (!scope || scope.type === 'overview') {
    return ensureOverviewLoaded();
  }
  return ensureShardLoaded(scope.type, scope.key);
}

async function performSearch(query, filters, scope) {
  let results = await getSearchDataset(scope);

  if (query) {
    const lowerQuery = query.toLowerCase();
    results = results.filter(item =>
      item.sentence.toLowerCase().includes(lowerQuery)
    );
  }

  if (filters.year) {
    results = results.filter(item => item.year === filters.year);
  }

  if (filters.minister) {
    results = results.filter(item => item.minister === filters.minister);
  }

  if (filters.ministry) {
    results = results.filter(item => item.ministry === filters.ministry);
  }

  const limit = scope && scope.type !== 'overview' ? 200 : 60;
  return results.slice(0, limit);
}

// Highlight matching text
function highlightText(text, query) {
  if (!query) return text;
  const regex = new RegExp(`(${query})`, 'gi');
  return text.replace(regex, '<mark>$1</mark>');
}
```

UI flow:
- On page load call `ensureOverviewLoaded()` so the first 60 answers appear instantly.
- Tapping "Expand to full archive" invokes `ensureShardLoaded('decades', decade)` or `ensureShardLoaded('topics', topic)` and refreshes results with the 200-result cap.
- We keep the overview data in memory; shards live in `shardCache` so subsequent toggles reuse the previously downloaded files.

**2. Chart Rendering (language.js, ministries.js, ministers.js)**

```javascript
// Plotly.js chart configuration
function renderReadabilityChart(data) {
  const trace = {
    x: data.map(d => d.year),
    y: data.map(d => d.flesch_score),
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Flesch Score',
    line: { color: '#2E86AB', width: 3 },
    marker: { size: 6 }
  };

  const layout = {
    title: 'Reading Ease Over Time',
    xaxis: { title: 'Year' },
    yaxis: { title: 'Flesch Score (Higher = Easier)' },
    hovermode: 'closest',
    font: { family: 'system-ui, sans-serif' }
  };

  Plotly.newPlot('readability-chart', [trace], layout, {
    responsive: true,
    displayModeBar: false
  });
}
```

**3. Progressive Statistics Loading**

```javascript
// Load statistics on demand
async function loadMinistryStats(ministry) {
  const statsPanel = document.getElementById(`stats-${ministry}`);

  if (statsPanel.dataset.loaded) return; // Already loaded

  const response = await fetch(`data/ministry_${ministry}.json`);
  const data = await response.json();

  // Render statistics
  statsPanel.innerHTML = renderStatsTable(data);
  statsPanel.dataset.loaded = 'true';
}

// Attach to details elements
document.querySelectorAll('.stats-panel').forEach(panel => {
  panel.addEventListener('toggle', function() {
    if (this.open) {
      const ministry = this.dataset.ministry;
      loadMinistryStats(ministry);
    }
  });
});
```

---

### Data Format Examples

**search-index/overview.json** (~150KB)
```json
[
  {
    "year": 1965,
    "sentence": "We will build new schools to secure our future workforce.",
    "minister": "Lim Kim San",
    "ministry": "education",
    "decade": "1960s"
  },
  // ... curated highlights across every decade
]
```

**search-index/decades/1960s.json**
```json
{
  "decade": "1960s",
  "sentences": [
    {
      "year": 1960,
      "sentence": "We must build a credible defence force to ensure our survival.",
      "minister": "Goh Keng Swee",
      "ministry": "defence"
    }
    // ... full 6,000+ sentences for the decade
  ]
}
```

**summary/ministries.json**
```json
{
  "1960s": {
    "defence": 21.4,
    "finance": 14.9,
    "education": 7.2
  },
  "1970s": {
    "defence": 17.6,
    "finance": 12.2,
    "education": 8.5
  }
  // ... all decades through 2020s
}
```

**detailed/ministries-1960s.json**
```json
{
  "1960": {
    "defence": 22.3,
    "finance": 15.8,
    "education": 6.2
  },
  "1961": {
    "defence": 20.4,
    "finance": 16.1,
    "education": 6.8
  }
  // ... each year in the decade
}
```

**summary/language.json**
```json
[
  {
    "decade": "1960s",
    "avg_flesch": 58.2,
    "avg_words_per_sentence": 22.1,
    "minister_count": 2
  },
  {
    "decade": "2020s",
    "avg_flesch": 64.7,
    "avg_words_per_sentence": 18.3,
    "minister_count": 2
  }
  // ... all decades
]
```

---

## GitHub Pages Deployment

### Deployment Strategy: `docs/` Folder Method

**Why `docs/` folder?**
- Keeps website separate from analysis code
- No need for separate `gh-pages` branch
- Easier to maintain and update

### Directory Structure
```
singapore-budget-speeches/
├── docs/                    # ← GitHub Pages serves from here
│   ├── index.html
│   ├── search.html
│   ├── ministries.html
│   ├── ministers.html
│   ├── language.html
│   ├── about.html
│   ├── assets/
│   │   ├── app.[hash].js
│   │   ├── vendor.[hash].js
│   │   └── style.[hash].css
│   └── data/
│       ├── summary/
│       │   ├── ministries.json
│       │   ├── ministers.json
│       │   ├── language.json
│       │   └── crises.json
│       ├── detailed/
│       │   ├── ministries-1960s.json
│       │   ├── ministers-focus.json
│       │   └── language-trends.json
│       └── search-index/
│           ├── overview.json
│           ├── decades/
│           │   ├── 1960s.json
│           │   └── ...
│           └── topics/
│               ├── social_support.json
│               └── ...
│
├── analysis/               # Jupyter notebooks (NOT deployed)
├── extractor/             # Python scripts (NOT deployed)
├── processor/             # Data processing (NOT deployed)
├── output_processor/      # Parquet files (NOT deployed)
├── src/                   # JS/CSS modules compiled by Vite
├── README.md              # Repository README
└── pyproject.toml
```

### Deployment Steps

```bash
# 1. Prepare docs/ for build outputs
mkdir -p docs/{assets,data}

# 2. Build hashed assets with Vite (outputs to docs/assets/)
npm install
npm run build

# 3. Run data export script (see next section)
cd analysis
python export_for_web.py
cd ..

# 4. Move/refresh HTML entry files
cp *.html docs/

# 5. Commit and push
git add docs/
git commit -m "Add website to docs/ for GitHub Pages"
git push origin main

# 6. Enable GitHub Pages
# Go to: github.com/parleh-mate/singapore-budget-speeches/settings/pages
# Source: main branch
# Folder: /docs
# Save

# 7. Wait 1-2 minutes, then visit:
# https://jeremychia.github.io/singapore-budget-speeches/
```

### Testing Locally

```bash
# Use Python's built-in server
cd docs
python -m http.server 8000

# Visit: http://localhost:8000
```

This simulates GitHub Pages and catches issues like:
- Incorrect file paths
- Missing data files
- JavaScript errors

---

## Data Export Pipeline

### Python Script: `analysis/export_for_web.py`

```python
"""
Export analysis data as lightweight summaries plus lazy-load shards.
"""
import json
from collections import defaultdict
from pathlib import Path
import pandas as pd
import sys

sys.path.append(str(Path.cwd().parent / 'extractor'))
from speech_links import budget_speech_links

web_data_dir = Path.cwd().parent / 'docs' / 'data'
summary_dir = web_data_dir / 'summary'
detailed_dir = web_data_dir / 'detailed'
search_dir = web_data_dir / 'search-index'
decade_dir = search_dir / 'decades'
topic_dir = search_dir / 'topics'

for target in [summary_dir, detailed_dir, decade_dir, topic_dir]:
  target.mkdir(parents=True, exist_ok=True)

def write_json(relative_path: Path, payload) -> None:
  path = web_data_dir / relative_path
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(payload, indent=2))
  print(f"  • {relative_path}")

def to_decade(year: int) -> str:
  return f"{int(year // 10 * 10)}s"

def to_slug(value: str) -> str:
  return value.lower().replace(' ', '_').replace('/', '_')

print("Starting data export for web (summaries first, full shards on demand)...\n")

# ============================================================================
# 1. MINISTRY DISTRIBUTIONS
# ============================================================================
print("Exporting ministry summaries + decade shards...")
ministry_by_decade = pd.read_csv('ministry_by_decade.csv', index_col=0)
ministry_summary = {
  f"{int(decade)}s": {
    ministry: round(float(pct), 1)
    for ministry, pct in row.items()
    if pct >= 3.0
  }
  for decade, row in ministry_by_decade.iterrows()
}
write_json(Path('summary/ministries.json'), ministry_summary)

ministry_by_year = pd.read_csv('ministry_by_year.csv', index_col=0)
ministry_by_year.index = ministry_by_year.index.astype(int)
for decade_start in range(1960, 2030, 10):
  decade_end = decade_start + 9
  window = ministry_by_year.loc[
    (ministry_by_year.index >= decade_start)
    & (ministry_by_year.index <= decade_end)
  ]
  if window.empty:
    continue
  payload = {
    str(year): {
      ministry: round(float(pct), 2)
      for ministry, pct in row.items()
    }
    for year, row in window.iterrows()
  }
  write_json(Path(f'detailed/ministries-{decade_start}s.json'), payload)

# ============================================================================
# 2. MINISTER FOCUS AREAS
# ============================================================================
print("\nExporting minister focus data...")
ministry_by_minister = pd.read_csv('ministry_by_minister.csv', index_col=0)
minister_summary = {}
for minister, row in ministry_by_minister.iterrows():
  sorted_pairs = sorted(row.items(), key=lambda kv: kv[1], reverse=True)[:4]
  minister_summary[minister] = {
    ministry: round(float(pct), 1) for ministry, pct in sorted_pairs
  }
write_json(Path('summary/ministers.json'), minister_summary)

minister_detail = {
  minister: {
    ministry: round(float(pct), 2)
    for ministry, pct in row.items()
  }
  for minister, row in ministry_by_minister.iterrows()
}
write_json(Path('detailed/ministers-focus.json'), minister_detail)

# ============================================================================
# 3. LANGUAGE CHARACTERISTICS
# ============================================================================
print("\nExporting linguistic summaries...")
yearly_stats = pd.read_csv('yearly_speech_statistics.csv')
yearly_stats['decade'] = yearly_stats['year'].apply(to_decade)

language_summary = []
for decade, group in yearly_stats.groupby('decade'):
  language_summary.append({
    'decade': decade,
    'avg_flesch': round(group['readability'].mean(), 2),
    'avg_words_per_sentence': round(group['avg_words_per_sentence'].mean(), 2),
    'speech_count': int(group['speech_id'].nunique()) if 'speech_id' in group else int(group['year'].nunique())
  })
write_json(Path('summary/language.json'), language_summary)

language_detail = [
  {
    'year': int(row['year']),
    'minister': row['minister'],
    'flesch_score': round(float(row['readability']), 2),
    'avg_words_per_sentence': round(float(row['avg_words_per_sentence']), 2)
  }
  for _, row in yearly_stats.iterrows()
]
write_json(Path('detailed/language-trends.json'), language_detail)

# ============================================================================
# 4. CRISIS + TIMING SNAPSHOTS
# ============================================================================
print("\nExporting crisis response summaries...")
crisis_stats = pd.read_csv('crisis_analysis.csv')
write_json(Path('summary/crises.json'), crisis_stats.to_dict(orient='records'))

timing_stats = pd.read_csv('minister_timing_stats.csv')
write_json(Path('detailed/minister-timing.json'), timing_stats.to_dict(orient='records'))

# ============================================================================
# 5. SEARCH INDEX SHARDS
# ============================================================================
print("\nExporting search overview + shards (this takes a minute)...")
output_processor_path = Path.cwd().parent / 'output_processor'
parquet_files = sorted(output_processor_path.glob('*.parquet'))

search_rows = []
for file in parquet_files:
  df = pd.read_parquet(file)
  for year, info in budget_speech_links.items():
    if year in df['year'].values:
      df.loc[df['year'] == year, 'minister'] = info['minister']
  for _, row in df.iterrows():
    topic = row.get('topic') or row.get('ministry') or 'general'
    record = {
      'year': int(row['year']),
      'sentence': row['sentence_text'],
      'minister': row.get('minister', ''),
      'ministry': row.get('ministry', ''),
      'topic': topic,
      'sentence_num': int(row.get('sentence_number', 0))
    }
    search_rows.append(record)

overview_limit = defaultdict(int)
overview = []
for record in search_rows:
  decade_label = to_decade(record['year'])
  if overview_limit[decade_label] >= 120:
    continue
  overview_limit[decade_label] += 1
  overview.append({**record, 'decade': decade_label})
write_json(Path('search-index/overview.json'), overview)

decade_buckets = defaultdict(list)
for record in search_rows:
  decade_buckets[to_decade(record['year'])].append(record)
for decade_label, sentences in decade_buckets.items():
  write_json(Path(f'search-index/decades/{decade_label}.json'), {
    'decade': decade_label,
    'sentences': sentences
  })

topic_buckets = defaultdict(list)
for record in search_rows:
  topic_buckets[record['topic']].append(record)
for topic, sentences in topic_buckets.items():
  write_json(Path(f"search-index/topics/{to_slug(topic)}.json"), {
    'topic': topic,
    'sentences': sentences
  })

print(f"✓ Overview sentences: {len(overview):,}")
print(f"✓ Full archive sentences: {len(search_rows):,}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("DATA EXPORT COMPLETE!")
print("="*70)
print(f"\nAll files exported to: {web_data_dir}")
print("\nKey folders:")
print("  • summary/           -> <=200KB bootstrap payloads")
print("  • detailed/          -> Decade/topic deep dives")
print("  • search-index/      -> Overview + decade/topic shards")
print("\nNext steps:")
print("  1. Create HTML entry files + run Vite build into docs/")
print("  2. Test locally: cd docs && python -m http.server 8000")
print("  3. Push to GitHub: git add docs/ && git commit && git push")
print("  4. Enable GitHub Pages in repository settings")
```

---

## Development Checklist

### Phase 1: Setup & Data Export ✓
- [x] Analyze data in Jupyter notebooks
- [x] Define website strategy (this document)
- [ ] Create `docs/` folder structure
- [ ] Run `export_for_web.py` script
- [ ] Verify JSON files created

### Phase 2: Core Pages 🚧
- [ ] **index.html** - Homepage with 3 entry paths
  - [ ] Hero section
  - [ ] 4 stat cards
  - [ ] 3 entry path cards
  - [ ] Quick questions section
- [ ] **search.html** - Search interface
  - [ ] Search box + filters
  - [ ] Results display with context
  - [ ] Statistics sidebar
- [ ] **ministries.html** - Ministry trends
  - [ ] Stacked area chart (Plotly)
  - [ ] Decade heatmap
  - [ ] Expandable statistics
- [ ] **ministers.html** - Minister comparison
  - [ ] Timeline
  - [ ] Minister profile cards
  - [ ] Comparison heatmap
- [ ] **language.html** - Linguistic analysis
  - [ ] 5 Plotly charts
  - [ ] Era timeline
  - [ ] Statistics panel
- [ ] **about.html** - Methodology & credits

### Phase 3: Styling & Polish ✨
- [ ] **src/style.css** (build → assets/style.[hash].css) - Design system
  - [ ] Color variables
  - [ ] Typography scale
  - [ ] Component styles
  - [ ] Responsive breakpoints
- [ ] Accessibility audit
  - [ ] Semantic HTML
  - [ ] ARIA labels
  - [ ] Keyboard navigation
  - [ ] Color contrast check

### Phase 4: JavaScript Functionality ⚙️
- [ ] **src/search.js** - Client-side search
  - [ ] Load overview JSON + shard fetchers
  - [ ] Filter, highlight, and paginate results
  - [ ] Wire "Expand archive" control to shard loader
- [ ] **src/language.js** - Linguistic charts
  - [ ] Render summary charts from summary/language.json
  - [ ] Fetch detailed trend shard when user expands
- [ ] **src/ministries.js** - Ministry charts
  - [ ] Seed stacked area with summary/ministries.json
  - [ ] Load decade shard on expand and update heatmap
- [ ] **src/ministers.js** - Minister charts
  - [ ] Timeline
  - [ ] Comparison heatmap fed by detailed/ministers-focus.json

### Phase 5: Testing & Refinement 🧪
- [ ] Local testing (`python -m http.server`)
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile responsiveness
- [ ] Performance optimization
  - [ ] Lazy load charts
  - [ ] Compress images (if any)
  - [ ] Minify CSS/JS (optional)
- [ ] Content proofread
- [ ] Link checking

### Phase 6: Deployment 🚀
- [ ] Push `docs/` to GitHub
- [ ] Enable GitHub Pages
- [ ] Verify live site works
- [ ] Test all links and features
- [ ] Share with initial users for feedback

### Phase 7: Iteration 🔄
- [ ] Collect user feedback
- [ ] Fix bugs
- [ ] Add requested features
- [ ] Update data (for future speeches)

---

## Success Metrics

### User Engagement Goals

**Storyteller Path (5 min):**
- 60% of visitors view at least 3 pages
- Average time on site: 5-7 minutes

**Explorer Path (15 min):**
- 30% of visitors interact with charts (hover/click)
- Average time on site: 12-18 minutes

**Researcher Path (30+ min):**
- 10% of visitors download CSV files
- 5% visit GitHub repository
- Average time on site: 25+ minutes

### Technical Performance

- Page load time: < 3 seconds (on 4G)
- Search results: < 1 second (for 40k sentences)
- Chart rendering: < 500ms
- Mobile-friendly (responsive design)

### Content Quality

- All statistics traced to source data
- No broken links
- Accessible (WCAG 2.1 AA)
- Clear methodology documentation

---

## Future Enhancements (Post-Launch)

### Short Term
1. **Export Charts**: Allow users to download chart images
2. **Share URLs**: Deep links to specific searches/ministers
3. **Print Styles**: Printer-friendly versions of pages
4. **Dark Mode**: Toggle for dark theme

### Medium Term
1. **Comparison Tool**: Side-by-side minister/year comparison
2. **Annotation Layer**: Expert commentary on key speeches
3. **API Endpoint**: JSON API for researchers
4. **Embed Widgets**: Embeddable charts for news articles

### Long Term
1. **NLP Analysis**: Sentiment, emotion, topic modeling
2. **Interactive Timeline**: Scroll-based storytelling
3. **Audio Integration**: Read-aloud feature
4. **Multi-language**: Chinese translation

---

## Open Questions / Decisions Needed

1. **Custom Domain**: Should we register `sgbudgetspeeches.com`?
2. **Analytics**: Use Google Analytics or privacy-focused alternative?
3. **Social Meta Tags**: OpenGraph for Twitter/Facebook sharing?
4. **Citation Format**: How should researchers cite this?
5. **Update Frequency**: Annual updates after each budget?

---

## Appendix: File Sizes

**Estimated file sizes for GitHub Pages:**

```
docs/
├── index.html                      ~16KB
├── search.html                     ~13KB
├── ministries.html                 ~18KB
├── ministers.html                  ~21KB
├── language.html                   ~16KB
├── about.html                      ~14KB
├── assets/
│   ├── app.[hash].js               ~32KB (routing + page shells)
│   ├── vendor.[hash].js            ~380KB (Plotly + utilities)
│   └── style.[hash].css            ~28KB (design tokens)
└── data/
  ├── summary/
  │   ├── ministries.json         ~12KB
  │   ├── ministers.json          ~4KB
  │   ├── language.json           ~3KB
  │   └── crises.json             ~2KB
  ├── detailed/
  │   ├── ministries-1960s.json   ~40KB
  │   ├── ministers-focus.json    ~15KB
  │   └── language-trends.json    ~18KB
  └── search-index/
    ├── overview.json           ~150KB
    ├── decades/
    │   ├── 1960s.json          ~480KB
    │   └── ...
    └── topics/
      ├── social_support.json ~320KB
      └── ...

Initial load: ~0.7MB (HTML + assets + summary payloads)
Full archive (all shards fetched): ~3.8MB
```

**Note:** Plotly.js ships inside vendor.[hash].js so every page reuses the same cached bundle.

---

## Contact & Collaboration

**Repository:** https://github.com/parleh-mate/singapore-budget-speeches

**Issues/Feedback:** GitHub Issues tab

**Contributions:** Pull requests welcome for:
- Bug fixes
- Design improvements
- Additional analysis
- Documentation

---

**Document Version:** 1.0
**Last Updated:** February 8, 2026
**Status:** Ready for Implementation

---

This strategy document serves as the blueprint for building the Singapore Budget Speeches website. All design decisions, technical choices, and content structures have been carefully considered to create a reader-centric experience that balances storytelling with statistical rigor.

**Next Step:** Review this strategy, make any final adjustments, then proceed to Phase 2 (Core Pages development).
