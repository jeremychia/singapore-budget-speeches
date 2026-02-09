// ===================================
// SEARCH PAGE WITH PROGRESSIVE LOADING
// Singapore Budget Speeches (1960-2025)
// ===================================

// Cache for loaded shards
const shardCache = new Map();

// Search state
let searchIndex = null;
let currentResults = [];

// Initialize search page
document.addEventListener('DOMContentLoaded', () => {
    loadSearchOverview();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    const hintButtons = document.querySelectorAll('.hint-button');
    const sortFilter = document.getElementById('sortFilter');
    
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
    
    // Re-sort and re-display results when sort option changes
    sortFilter.addEventListener('change', () => {
        if (window.currentResults && window.currentResults.length > 0) {
            resortAndDisplayResults();
        }
    });
    
    hintButtons.forEach(button => {
        button.addEventListener('click', () => {
            const query = button.dataset.query;
            searchInput.value = query;
            performSearch();
        });
    });
}

// Re-sort current results and re-display them
function resortAndDisplayResults() {
    const sortFilter = document.getElementById('sortFilter').value;
    sortResults(window.currentResults, sortFilter);
    displayResults(window.currentResults, window.currentQuery);
}

// Load search index overview (lightweight)
async function loadSearchOverview() {
    try {
        const response = await fetch('data/search-index/overview.json');
        searchIndex = await response.json();
        console.log('Search index overview loaded');
    } catch (error) {
        console.error('Failed to load search index:', error);
        showError('Failed to load search index. Please refresh the page.');
    }
}

// Perform search
async function performSearch() {
    const query = document.getElementById('searchInput').value.trim().toLowerCase();
    const decadeFilter = document.getElementById('decadeFilter').value;
    const ministerFilter = document.getElementById('ministerFilter').value;
    const topicFilter = document.getElementById('topicFilter').value;
    const sortFilter = document.getElementById('sortFilter').value;
    
    if (!query) {
        showStatus('Please enter a search term');
        return;
    }
    
    showStatus('Searching...');
    
    try {
        // Determine which shards to load
        const shardsToLoad = determineShards(decadeFilter, topicFilter);
        
        // Load required shards
        await loadShards(shardsToLoad);
        
        // Execute search
        const results = executeSearch(query, decadeFilter, ministerFilter, topicFilter, sortFilter);
        
        // Display results
        displayResults(results, query);
        
    } catch (error) {
        console.error('Search error:', error);
        showError('Search failed. Please try again.');
    }
}

// Determine which shards to load based on filters
function determineShards(decade, topic) {
    const shards = [];
    
    if (decade) {
        shards.push(`decades/${decade}.json`);
    } else {
        // Load all decade shards
        ['1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'].forEach(d => {
            shards.push(`decades/${d}.json`);
        });
    }
    
    if (topic) {
        shards.push(`topics/${topic.toLowerCase().replace(/\s+/g, '-')}.json`);
    }
    
    return shards;
}

// Load shards (with caching)
async function loadShards(shardPaths) {
    const loadPromises = shardPaths.map(async (path) => {
        if (shardCache.has(path)) {
            return shardCache.get(path);
        }
        
        try {
            const response = await fetch(`data/search-index/${path}`);
            const data = await response.json();
            shardCache.set(path, data);
            return data;
        } catch (error) {
            console.error(`Failed to load shard: ${path}`, error);
            return null;
        }
    });
    
    return Promise.all(loadPromises);
}

// Execute search across loaded data
function executeSearch(query, decadeFilter, ministerFilter, topicFilter, sortFilter) {
    const results = [];
    const queryTerms = query.toLowerCase().split(/\s+/);
    
    // Search through cached shards
    shardCache.forEach((shard, path) => {
        if (!shard || !shard.sentences) return;
        
        shard.sentences.forEach(sentence => {
            // Apply decade filter
            if (decadeFilter && !sentence.year.toString().startsWith(decadeFilter.slice(0, 3))) {
                return;
            }
            
            // Apply minister filter
            if (ministerFilter && sentence.minister !== ministerFilter) {
                return;
            }
            
            // Apply topic filter
            if (topicFilter && sentence.topic !== topicFilter) {
                return;
            }
            
            // Check if sentence matches query
            const text = sentence.text.toLowerCase();
            const matches = queryTerms.every(term => text.includes(term));
            
            if (matches) {
                // Calculate relevance score
                const score = calculateRelevance(sentence.text, queryTerms);
                results.push({ ...sentence, score });
            }
        });
    });
    
    // Sort results
    sortResults(results, sortFilter);
    
    return results;
}

// Sort results based on selected option
function sortResults(results, sortBy) {
    switch (sortBy) {
        case 'year-desc':
            results.sort((a, b) => b.year - a.year || b.score - a.score);
            break;
        case 'year-asc':
            results.sort((a, b) => a.year - b.year || b.score - a.score);
            break;
        case 'minister':
            results.sort((a, b) => {
                const ministerCompare = (a.minister || '').localeCompare(b.minister || '');
                return ministerCompare !== 0 ? ministerCompare : b.score - a.score;
            });
            break;
        case 'topic':
            results.sort((a, b) => {
                const topicCompare = (a.topic || '').localeCompare(b.topic || '');
                return topicCompare !== 0 ? topicCompare : b.score - a.score;
            });
            break;
        case 'relevance':
        default:
            results.sort((a, b) => b.score - a.score);
            break;
    }
}

// Calculate relevance score
function calculateRelevance(text, terms) {
    let score = 0;
    const lowerText = text.toLowerCase();
    
    terms.forEach(term => {
        // Exact phrase match
        if (lowerText.includes(terms.join(' '))) {
            score += 10;
        }
        
        // Individual term matches
        const matches = (lowerText.match(new RegExp(term, 'g')) || []).length;
        score += matches * 2;
        
        // Bonus for term at start of sentence
        if (lowerText.startsWith(term)) {
            score += 5;
        }
    });
    
    return score;
}

// Topic colours for badges (civic strength palette with lighter tints for badges)
const topicColors = {
    'Defence': { bg: '#FADCDC', text: '#C8102E' },
    'Education': { bg: '#D9E4ED', text: '#0C2340' },
    'Health': { bg: '#D4E8DE', text: '#2D6A4F' },
    'Housing': { bg: '#F5ECD4', text: '#B8941A' },
    'Transport': { bg: '#D9E8EB', text: '#3D7C8C' },
    'Economy': { bg: '#DDE5ED', text: '#1A3A5C' },
    'Finance': { bg: '#E5DDE7', text: '#6B4E71' },
    'Social Services': { bg: '#F2E0D8', text: '#B45A3C' },
    'Environment': { bg: '#D4E8DE', text: '#2D6A4F' },
    'Technology': { bg: '#E5E5E5', text: '#5C5C5C' },
    'General': { bg: '#EDECEA', text: '#4A5568' }
};

function getTopicBadge(topic) {
    const colors = topicColors[topic] || topicColors['General'];
    return `<span class="topic-badge" style="background-color: ${colors.bg}; color: ${colors.text}">${topic}</span>`;
}

// Display search results
function displayResults(results, query) {
    const container = document.getElementById('searchResults');
    
    if (results.length === 0) {
        showStatus(`No results found for "${query}"`);
        container.innerHTML = '';
        return;
    }
    
    showStatus(`Found ${results.length} result${results.length !== 1 ? 's' : ''} for "${query}"`);
    
    // Store results globally for context lookup
    window.currentResults = results;
    window.currentQuery = query;
    
    // Limit to top 100 results
    const displayResults = results.slice(0, 100);
    
    container.innerHTML = displayResults.map((result, index) => `
        <div class="search-result-item" data-index="${index}">
            <div class="search-result-meta">
                <span class="result-info">
                    <strong>${result.year}</strong> · ${result.minister || 'Unknown Minister'}
                </span>
                <span class="result-actions">
                    ${getTopicBadge(result.topic || 'General')}
                    <button class="context-toggle" onclick="toggleContext(${index})" title="Show more context">
                        ▼ Context
                    </button>
                </span>
            </div>
            <div class="search-result-text">
                ${highlightQuery(result.text, query)}
            </div>
            <div class="search-result-context" id="context-${index}" style="display: none;">
                <div class="context-loading">Loading context...</div>
            </div>
        </div>
    `).join('');
    
    if (results.length > 100) {
        container.innerHTML += `
            <div class="search-result-item" style="text-align: center; background: var(--color-bg-alt); border-left: none;">
                <em>Showing top 100 of ${results.length} results. Refine your search for more specific results.</em>
            </div>
        `;
    }
}

// Toggle context expansion
async function toggleContext(index) {
    const contextDiv = document.getElementById(`context-${index}`);
    const button = document.querySelector(`[data-index="${index}"] .context-toggle`);
    
    if (contextDiv.style.display === 'none') {
        contextDiv.style.display = 'block';
        button.textContent = '▲ Hide Context';
        button.classList.add('active');
        
        // Load context if not already loaded
        if (contextDiv.querySelector('.context-loading')) {
            await loadContext(index);
        }
    } else {
        contextDiv.style.display = 'none';
        button.textContent = '▼ Show Context';
        button.classList.remove('active');
    }
}

// Load surrounding context for a result
async function loadContext(index) {
    const result = window.currentResults[index];
    const contextDiv = document.getElementById(`context-${index}`);
    
    if (!result) return;
    
    // Get all sentences from the same year in the cache
    const decade = result.decade;
    const shardPath = `decades/${decade}.json`;
    
    // Ensure shard is loaded
    if (!shardCache.has(shardPath)) {
        try {
            const response = await fetch(`data/search-index/${shardPath}`);
            const data = await response.json();
            shardCache.set(shardPath, data);
        } catch (error) {
            contextDiv.innerHTML = '<em>Failed to load context</em>';
            return;
        }
    }
    
    const shard = shardCache.get(shardPath);
    if (!shard || !shard.sentences) {
        contextDiv.innerHTML = '<em>Context not available</em>';
        return;
    }
    
    // Find sentences from the same year
    const yearSentences = shard.sentences.filter(s => s.year === result.year);
    
    // Find the index of the current sentence
    const currentIdx = yearSentences.findIndex(s => s.text === result.text);
    
    if (currentIdx === -1) {
        contextDiv.innerHTML = '<em>Context not available</em>';
        return;
    }
    
    // Get surrounding sentences (3 before, 3 after)
    const contextRange = 3;
    const startIdx = Math.max(0, currentIdx - contextRange);
    const endIdx = Math.min(yearSentences.length - 1, currentIdx + contextRange);
    
    const contextSentences = yearSentences.slice(startIdx, endIdx + 1);
    
    // Build context HTML
    const contextHtml = contextSentences.map((sentence, i) => {
        const actualIdx = startIdx + i;
        const isCurrent = actualIdx === currentIdx;
        const text = isCurrent 
            ? highlightQuery(sentence.text, window.currentQuery)
            : sentence.text;
        
        return `<p class="${isCurrent ? 'context-current' : 'context-surrounding'}">${text}</p>`;
    }).join('');
    
    contextDiv.innerHTML = `
        <div class="context-content">
            <div class="context-header">
                <strong>📄 ${result.year} Budget Speech</strong> — ${result.minister}
            </div>
            ${contextHtml}
            <div class="context-footer">
                <a href="https://github.com/jeremychia/singapore-budget-speeches/blob/main/output_markdown/${result.year}.md" 
                   target="_blank" class="view-full-speech">
                    View Full Speech →
                </a>
            </div>
        </div>
    `;
}

// Highlight query terms in text
function highlightQuery(text, query) {
    const terms = query.toLowerCase().split(/\s+/);
    let highlighted = text;
    
    terms.forEach(term => {
        const regex = new RegExp(`(${escapeRegex(term)})`, 'gi');
        highlighted = highlighted.replace(regex, '<mark>$1</mark>');
    });
    
    return highlighted;
}

// Escape special regex characters
function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Show status message
function showStatus(message) {
    const statusElement = document.getElementById('searchStatus');
    statusElement.textContent = message;
    statusElement.style.color = 'var(--color-text-light)';
}

// Show error message
function showError(message) {
    const statusElement = document.getElementById('searchStatus');
    statusElement.textContent = message;
    statusElement.style.color = 'var(--color-error)';
}
